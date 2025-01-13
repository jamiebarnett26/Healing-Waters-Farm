
from top import app, oauth
import flask
from flask import redirect
from flask_session import Session
import database
import sys
import os

app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    SESSION_TYPE='filesystem',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
Session(app)

@app.route('/login')
def login():
    print('Login', file=sys.stderr)
    google = oauth.create_client('google')
    redirect_uri = flask.url_for('authorize_login', _external=True)
    return google.authorize_redirect(redirect_uri)



@app.route('/authorize_login')
def authorize_login():
    try:
        google = oauth.create_client('google')
        token = google.authorize_access_token()
        resp = google.get('userinfo', token=token)
        resp.raise_for_status()
        user_info = resp.json()
    except Exception as e:
        return flask.abort(401, f"Authorization failed: {str(e)}")

    email = user_info.get('email')
    first_name = user_info.get('given_name','')
    last_name = user_info.get('family_name','')

    flask.session['first_name'] = first_name
    flask.session['last_name'] = last_name
    flask.session['email'] = email
    
    user = database.get_user(email, 'email')
    if user:
        resp = flask.make_response(flask.redirect('/homepage'))
        resp.set_cookie('user_id', str(user.user_id))
        admin = database.is_admin(user.user_id)
        resp.set_cookie('admin', admin, httponly=True, secure=True, max_age=3600)
        return resp
    else:
        user = database.add_user(first_name, last_name, email)
        
    resp = flask.make_response(flask.redirect('/homepage'))
    resp.set_cookie('user_id', str(user.user_id), httponly=True, secure=True, max_age=3600)
    return resp

     
#-----------------------------------------------------------------------

@app.route('/logout', methods=['POST'])
def logout():
    flask.session.clear()
    resp = flask.make_response(flask.redirect('https://accounts.google.com/Logout'))
    resp.set_cookie('user_id', '', expires=0)
    resp.set_cookie('admin', '', expires=0)
    return resp