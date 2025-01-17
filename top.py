import flask
from authlib.integrations.flask_client import OAuth
from flask import redirect, url_for

app = flask.Flask(__name__, template_folder='templates')


@app.route('/manifest.json')
def serve_manifest():
    return flask.send_from_directory('.', 'manifest.json')

@app.route('/serviceWorker.js')
def serve_serviceWorker():
    return flask.send_from_directory('.', 'serviceWorker.js')

# oauth config for google
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='272340197272-0n57ghndnfe5q06928eubf4nac3ig39o.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'profile email'}
)