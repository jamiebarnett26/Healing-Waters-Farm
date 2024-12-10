from top import app, oauth
import flask
from flask import redirect
import database
import time
import json
import sys
import datetime

def get_current_time():
    return time.asctime(time.localtime())

# edit for flask route with 
@app.route('/getTasks/<user_crop_id>', methods=['GET'])
def get_tasks(user_crop_id):
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    
    todos = []

    print(type(user_crop_id))
    print(user_crop_id)

    todos = database.get_tasks(user_crop_id)

    if len(todos) == 0:
       todos.append({"task": "nothing", "date": "nothing", "done": "not done"})

    return flask.jsonify(todos)