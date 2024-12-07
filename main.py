import gevent.monkey; gevent.monkey.patch_all()
import bottle, dataclasses, os, dotenv, requests, githubchecker
import jwt, json, time

dotenv.load_dotenv()

TURNSTILE_KEY = os.getenv("TURNSTILE_KEY")
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET")
PORT = os.getenv("PORT", 8080)

# Cloudflare Access
ACCESS_POLICY_AUD = os.getenv("POLICY_AUD")
ACCESS_TEAM_DOMAIN = os.getenv("TEAM_DOMAIN")
ACCESS_CERTS_URL = "{}/cdn-cgi/access/certs".format(ACCESS_TEAM_DOMAIN)

def _get_public_keys():
    """
    Returns:
        List of RSA public keys usable by PyJWT.
    """
    r = requests.get(ACCESS_CERTS_URL)
    public_keys = []
    jwk_set = r.json()
    for key_dict in jwk_set['keys']:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
        public_keys.append(public_key)
    return public_keys

def verify_access_token(f):
    def wrapper(*args, **kwargs):
        access_token = bottle.request.get_header("Cf-Access-Jwt-Assertion", bottle.request.get_cookie("CF_Authorization"))
        if not access_token:
            return bottle.HTTPError(403, "Forbidden")
        public_keys = _get_public_keys()
        for public_key in public_keys:
            try:
                payload = jwt.decode(access_token, public_key, audience=ACCESS_POLICY_AUD)
                # Check if the user is a member of the team
                if payload["groups"] and "everyone" not in payload["groups"]:
                    return bottle.HTTPError(403, "Forbidden")
                payload["email"] = payload["email"].lower()
                kwargs["payload"] = payload
                # check timestamps
                now = int(time.time())
                if now < payload["iat"] or now > payload["exp"]:
                    return bottle.HTTPError(403, "Forbidden")
                return f(*args, **kwargs)
            except jwt.exceptions.InvalidTokenError:
                continue
        return bottle.HTTPError(403, "Forbidden")
    return wrapper
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


@app.route("/")
def index():
    return bottle.template("index.tpl.html")


@app.route("/about")
def about():
    return bottle.template("about.tpl.html")

@app.route("/blog")
@app.route("/blag") # xkcd reference
def blag():
    return bottle.template("blog.tpl.html")

@app.route("/3d")
def three_d():
    return bottle.template("3dmodel.tpl.html")

@app.error(404)
@app.error(403)
@app.error()
def error(error):
    return bottle.template("error.tpl.html", error=error, code=error.status_code, message=error.body)



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
@verify_access_token
def admin(payload=None):
    return bottle.template("admin.tpl.html", payload=payload)

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
