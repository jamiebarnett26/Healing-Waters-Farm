from top import app, oauth
import flask
from flask import redirect
import database
import time
import json
import sys
import datetime

# edit for flask route with 
@app.route('/getTasks/<user_crop_id>', methods=['GET'])
def get_tasks(user_crop_id):
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    
    todos = []
    todos = database.get_tasks(user_crop_id)
    if len(todos) == 0:
       todos.append({"task": "nothing", "date": "nothing", "done": "not done"})

    todos = sorted(todos, key=lambda todo: (todo['completed'], todo['date']))
    return flask.jsonify(todos)


# Helper function, returns crop to do list for cards
@app.route('/checked', methods=['POST'])
def checked():
    data = flask.request.get_json()
    task_id = data.get('task_id')
    completed = data.get('completed')

    database.checkbox(task_id, completed)
    
    return flask.jsonify({
        'success': True,
        'completed': completed  # Return the updated status of the task
    })
