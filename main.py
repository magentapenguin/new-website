import gevent.monkey # isort:skip
gevent.monkey.patch_all() 
import dataclasses
import os

import bottle
import dotenv
import requests
import descope

import githubchecker

dotenv.load_dotenv()

TURNSTILE_KEY = os.getenv("TURNSTILE_KEY")
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")
PORT = int(os.getenv("PORT", "8080"))
DESCOPE_KEY = os.getenv("DESCOPE_KEY")
descope_client = descope.DescopeClient(DESCOPE_KEY)

@dataclasses.dataclass
class Project:
    name: str
    description: str
    image: str | None = None
    url: str | None = None
    github: str | None = None
    itch: str | None = None


bottle.TEMPLATE_PATH.insert(0, "views")
app = bottle.default_app()

def require_auth(f):
    def wrapper(*args, **kwargs):
        token = bottle.request.headers.get("Authorization")
        if not descope_client.validate_session(token):
            return bottle.HTTPError(403, "Forbidden")
        return f(*args, **kwargs)

    return wrapper

@app.route("/")
def index():
    return bottle.template("index.tpl.html")


@app.route("/about")
def about():
    return bottle.template("about.tpl.html")


@app.route("/blog")
@app.route("/blag")  # xkcd reference
def blag():
    return bottle.template("blog.tpl.html")


@app.route("/3d")
def three_d():
    return bottle.template("3dmodel.tpl.html")


@app.error(404)
@app.error(403)
@app.error()
def error(err):
    return bottle.template(
        "error.tpl.html", error=err, code=err.status_code, message=err.body
    )


@app.route("/contact", method=["GET", "POST"])
def contact():
    if bottle.request.method == "POST":
        # Get the form data
        token = bottle.request.forms.get("cf-turnstile-response")
        ip = bottle.request.headers.get("CF-Connecting-IP")
        if not token:
            return bottle.template(
                "contact.tpl.html",
                TURNSTILE_KEY=TURNSTILE_KEY,
                error="Please complete the CAPTCHA.",
            )
        # Verify the token
        url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        result = requests.post(
            url,
            json={"response": token, "secret": TURNSTILE_SECRET, "remoteip": ip},
            timeout=5,
        )
        if not result.json()["success"]:
            return bottle.template(
                "contact.tpl.html",
                TURNSTILE_KEY=TURNSTILE_KEY,
                error="CAPTCHA verification failed.",
            )
    return bottle.template("contact.tpl.html", TURNSTILE_KEY=TURNSTILE_KEY)


@app.route("/admin")
@require_auth
def admin():
    return bottle.template("admin.tpl.html")

@app.route("/signup")
def signup():
    return bottle.template("signup.tpl.html",DESCOPE_KEY=DESCOPE_KEY)

@app.route("/projects")
def projects():
    return bottle.template(
        "projects.tpl.html",
        projects=[
            Project(
                name="Lorem Ipsum",
                description="A 2d top-down shooter game. Made with Kaplay.js.",
                image="/static/lorem.png",
                url="https://lorem-ipsum-game.magentapenguin.partykit.dev",
                github="https://github.com/magentapenguin/Lorem",
            ),
            Project(
                name="Chat",
                description="A work-in-progress chat application. Made with JavaScript.",
                url="https://chat.magentapenguin.partykit.dev",
                github="https://github.com/magentapenguin/chat",
            ),
            Project(
                name="Portfolio",
                description="This website! Made with Python and Bottle.",
                url="https://cat5python.com",
                github="https://github.com/magentapenguin/new-website",
            ),
            Project(
                name="Stickman Jump Game",
                description="A simple platformer game. Made with Kaboom.js. Development on hold.",
                image="/static/jumpgame.png",
                itch="https://magentapenguin.itch.io/platformer",
                github="https://github.com/magentapenguin/my-coding-stuff/tree/main/platformer",
            ),
        ],
    )


@app.route("/static/<filename:path>")
def static(filename):
    return bottle.static_file(filename, root="static")


githubchecker.main()
if __name__ == "__main__":
    bottle.run(app=app, host="0.0.0.0", port=PORT, debug=True, server="gevent")
