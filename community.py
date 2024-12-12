
from top import app, oauth
import flask
from flask import redirect, url_for
import data_community as database
import time
import json
import sys


#-----------------------------------------------------------------------
@app.route('/community', methods=['GET'])
def community():
    admin = flask.request.cookies.get('admin') == 'true'
    user_id = flask.request.cookies.get('user_id')

    if not user_id:
        return flask.redirect('/login')
    user = database.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
     
    user_name = user.first_name + " " + user.last_name
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
def add_question(user_id):
    title = flask.request.form.get('title_add')
    text = flask.request.form.get('text')
    if not user_id:
        return flask.redirect('/login')
    user = database.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
    print(title, file=sys.stderr)
    print(text, file=sys.stderr)
    user_name = user.first_name + " " + user.last_name
    question = {'user_id':user_id, 'user_name':user_name, 'title':title, 'text':text, 'status':'Unresolved'}
    database.add_question(question)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/addreply/<question_id>', methods=['POST'])
def add_reply(question_id):
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    user = database.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
     
    user_name = user.first_name + " " + user.last_name
    text = flask.request.form.get('text')
    reply = {'question_id':question_id,'user_id':user_id, 'user_name':user_name, 'text':text}
    database.add_reply(reply)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/addannouncement/', methods=['POST'])
def add_announcement():
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    user = database.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
     
    user_name = user.first_name + " " + user.last_name
    text = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'user_id':user_id, 'user_name':user_name, 'text':text, 'title':title}
    database.add_announcement(announcement)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/editquestion/<question_id>', methods=['POST'])
def post_edit_question(question_id):
    title = flask.request.form.get('title')
    text  = flask.request.form.get('text')
    question = {'title':title, 'text':text}
    database.edit_question(question_id, question)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------

@app.route('/editreply/<reply_id>', methods=['POST'])
def post_edit_reply(reply_id):
    text  = flask.request.form.get('text')
    reply = {'text':text}
    database.edit_reply(reply_id, reply)
    return redirect(url_for('community'))
    
#-----------------------------------------------------------------------

@app.route('/editannouncement/<announcement_id>', methods=['POST'])
def post_edit_announcement(announcement_id):
    text  = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'text':text, 'title':title}
    database.edit_announcement(announcement_id, announcement)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deletequestion/<question_id>', methods=['POST'])
def delete_question(question_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_question(user_id, question_id)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deletereply/<reply_id>', methods=['POST'])
def delete_reply(reply_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_reply(user_id, reply_id)
    return redirect(url_for('community'))

#-----------------------------------------------------------------------
@app.route('/deleteannouncement/<announcement_id>', methods=['POST'])
def delete_announcement(announcement_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_announcement(user_id, announcement_id)
    return redirect(url_for('community'))


