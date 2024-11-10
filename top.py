import flask
from authlib.integrations.flask_client import OAuth
app = flask.Flask(__name__, template_folder='templates')


@app.route('/manifest.json')
def serve_manifest():
    return flask.send_from_directory('.', 'manifest.json')

@app.route('/serviceWorker.js')
def serve_serviceWorker():
    return flask.send_from_directory('.', 'serviceWorker.js')

# TODO: Generate a secret random key
app.secret_key = 'random secret'

# oauth config for google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='144993838713-mvb15a64nvp0t5jd7j1spj4vr8pg7hdv.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'profile email'}
)