import bottle, dataclasses, os, dotenv, requests

dotenv.load_dotenv()

TURNSTILE_KEY = os.getenv('TURNSTILE_KEY')
TURNSTILE_SECRET = os.getenv('TURNSTILE_SECRET')

@dataclasses.dataclass
class Project:
    name: str
    description: str
    image: str
    url: str | None = None
    github: str | None = None
    itch: str | None = None

bottle.TEMPLATE_PATH.insert(0, 'views')
app = bottle.default_app()

@app.route('/')
def index():
    return bottle.template('index.tpl.html')

@app.route('/about')
def about():
    return bottle.template('about.tpl.html')

@app.route('/3d')
def three_d():
    return bottle.template('3dmodel.tpl.html')

@app.route('/contact', method=['GET', 'POST'])
def contact():
    if bottle.request.method == 'POST':
        # Get the form data
        token = bottle.request.forms.get('cf-turnstile-response')
        ip = bottle.request.headers.get('CF-Connecting-IP')
        if not token:
            return bottle.template('contact.tpl.html', TURNSTILE_KEY=TURNSTILE_KEY, error='Please complete the CAPTCHA.')
        # Verify the token
        url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        result = requests.post(url, json={'response': token, 'secret': TURNSTILE_SECRET, 'remoteip': ip})

    return bottle.template('contact.tpl.html', TURNSTILE_KEY=TURNSTILE_KEY)


@app.route('/projects')
def projects():
    return bottle.template('projects.tpl.html', projects=[
        Project(
            name='Lorem Ipsum',
            description='A 2d top-down shooter game. Made with Kaplay.js.',
            image='/static/lorem.png',
            url='https://lorem-ipsum-game.magentapenguin.partykit.dev',
            github='https://github.com/magentapenguin/Lorem',
            ),
        Project(
            name='Chat',
            description='A work-in-progress chat application. Made with JavaScript.',
            image='/static/placeholder.png',
            url='https://chat.magentapenguin.partykit.dev',
            github='https://github.com/magentapenguin/chat',
            ),
        Project(
            name='Portfolio',
            description='This website! Made with Python and Bottle.',
            image='/static/placeholder.png',
            url='https://cat5python.com',
            github='https://github.com/magentapenguin/new-website',
            ),
        Project(
            name='Stickman Jump Game',
            description='A simple platformer game. Made with Kaboom.js. Development on hold.',
            image='/static/jumpgame.png',
            itch='https://magentapenguin.itch.io/platformer',
            github='https://github.com/magentapenguin/my-coding-stuff/tree/main/platformer',
            ),
    ])

@app.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static')



if __name__ == '__main__':
    bottle.run(app=app, host='0.0.0.0', port=8080, debug=True)