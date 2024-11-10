
from top import app, oauth
import flask
from flask import redirect
import database
import sys

@app.route('/login')
def login():
    print('Login', file=sys.stderr)
    google = oauth.create_client('google')
    redirect_uri = flask.url_for('authorize_login', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/signup')
def signup():
    google = oauth.create_client('google')
    redirect_uri = flask.url_for('authorize_signin', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize_login')
def authorize_login():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    resp.raise_for_status()
    user_info = resp.json()

    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    flask.session['first_name'] = first_name
    flask.session['last_name'] = last_name
    flask.session['email'] = email
    
    user = database.get_user(email, 'email')
    if user:
        resp = flask.make_response(flask.redirect('/home'))
        resp.set_cookie('user_id', str(user.user_id))
        admin = database.is_admin(user.user_id)
        resp.set_cookie('admin', admin)
        return resp
    
    return redirect('signup')
     
@app.route('/authorize_signin')
def authorize_signin():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    resp.raise_for_status()
    user_info = resp.json()

    email = user_info.get('email')
    first_name = user_info.get('given_name')
    last_name = user_info.get('family_name')

    flask.session['first_name'] = first_name
    flask.session['last_name'] = last_name
    flask.session['email'] = email
    
    user = database.get_user(email, 'email')
    if user:
        return flask.redirect('/login')
    user = database.add_user(first_name, last_name, email)
    if not user:
        return flask.redirect('/signup')
    resp = flask.make_response(flask.redirect('/home'))
    resp.set_cookie('user_id', str(user.user_id))
    resp.set_cookie('admin', 'false')
    return resp
    

#-----------------------------------------------------------------------

@app.route('/logout')
def logout():
    flask.session.clear()
    resp = flask.make_response(flask.redirect('https://accounts.google.com/Logout'))
    resp.set_cookie('user_id', '', expires=0)
    resp.set_cookie('admin', '', expires=0)
    return resp