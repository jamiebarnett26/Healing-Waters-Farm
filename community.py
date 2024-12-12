
from top import app, oauth
import flask
from flask import redirect, url_for, Blueprint
import data_community as database
import database as datauser
import time
import json
import sys



#-----------------------------------------------------------------------
def get_current_time():
    return time.asctime(time.localtime())

def verify_admin():
    if flask.request.cookies.get('admin') != 'true':
        return "Custom 405 Method Not Allowed Error", 405

def verify_login():
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    user = datauser.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
 
def get_username(user_id):
    user = database.get_user(user_id, 'user_id')
    return user.first_name + " " + user.last_name

@app.route('/community', methods=['GET'])
def community():
    verify_login()
    admin = flask.request.cookies.get('admin') == 'true'
    user_id = flask.request.cookies.get('user_id')
    user_name = user_id
    questions = database.get_questions()
    replies = database.get_replies()
    announcements = database.get_announcements()
    html_code = flask.render_template('community.html',
                                      admin=admin,
                                      questions=questions,
                                      replies=replies,
                                      announcements=announcements,
                                      user_id=user_id,
                                      user_name=user_name,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/addquestion/<user_id>', methods=['POST'])
def add_question():
    verify_login()
    user_id = flask.request.cookies.get('user_id')
    title = flask.request.form.get('title_add')
    text = flask.request.form.get('text')
    user_name = user_id
    question = {'user_id':user_id, 'user_name':user_name, 'title':title, 'text':text, 'status':'Unresolved'}
    database.add_question(question)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/addreply/<question_id>', methods=['POST'])
def add_reply(question_id):
    verify_login()
    verify_admin()
    user_id = flask.request.cookies.get('user_id')
    user_name = user_id

    text = flask.request.form.get('text')
    reply = {'question_id':question_id,'user_id':user_id, 'user_name':user_name, 'text':text}
    database.add_reply(reply)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/addannouncement/', methods=['POST'])
def add_announcement():
    verify_login()
    verify_admin()
    user_id = flask.request.cookies.get('user_id')
    user_name = user_id
    text = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'user_id':user_id, 'user_name':user_name, 'text':text, 'title':title}
    database.add_announcement(announcement)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/editquestion/<question_id>', methods=['POST'])
def edit_question(question_id):
    verify_login()
    user_id = flask.request.cookies.get('user_id')
    admin = flask.request.cookies.get('admin') == 'true'
    user_question = database.search_field_id('question', question_id)[0]
    if not admin and user_id != user_question['user_id']:
        return "Custom 405 Method Not Allowed Error", 405
    title = flask.request.form.get('title')
    text  = flask.request.form.get('text')
    question = {'title':title, 'text':text}
    database.edit_question(question_id, question)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/editreply/<reply_id>', methods=['POST'])
def edit_reply(reply_id):
    verify_login()
    verify_admin()
    text  = flask.request.form.get('text')
    reply = {'text':text}
    database.edit_reply(reply_id, reply)
    return redirect(url_for('community'))
    
#-----------------------------------------------------------------------

@app.route('/editannouncement/<announcement_id>', methods=['POST'])
def edit_announcement(announcement_id):
    verify_login()
    verify_admin()
    text  = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'text':text, 'title':title}
    database.edit_announcement(announcement_id, announcement)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deletequestion/<question_id>', methods=['POST'])
def delete_question(question_id):
    verify_login()
    user_id = flask.request.cookies.get('user_id')
    admin = flask.request.cookies.get('admin') == 'true'
    user_question = database.search_field_id('question', question_id)[0]
    if (not admin) and user_id != user_question['user_id']:
        return "Custom 405 Method Not Allowed Error", 405
    database.delete_question(user_id, question_id)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deletereply/<reply_id>', methods=['POST'])
def delete_reply(reply_id):
    verify_login()
    verify_admin()
    user_id = flask.request.cookies.get('user_id')
    database.delete_reply(user_id, reply_id)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deleteannouncement/<announcement_id>', methods=['POST'])
def delete_announcement(announcement_id):
    verify_login()
    verify_admin()
    user_id = flask.request.cookies.get('user_id')
    database.delete_announcement(user_id, announcement_id)
    return redirect(url_for('community'))


