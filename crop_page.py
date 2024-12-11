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
       return flask.jsonify(todos)

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
        'completed': completed  # returning updated status of the task
    })

@app.route('/updateCropInfo', methods = ['POST'])
def update_crop_info():

    data = flask.request.get_json()
    variety_name = data.get('variety_name')
    variety_id = data.get('variety_id')
    updated_info = data.get('updated_fields')

    print("updated_info is:", updated_info)

    variety = {'variety_name':variety_name}

    database.edit_variety(variety_id, variety, updated_info)

    return flask.jsonify({
        'success': True,
    })

@app.route('/addTask', methods=['POST'])
def add_task_page():
    data = flask.request.get_json()
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')

    task_name = data.get('task_name')
    task_date = data.get('task_date')
    user_crop_id = data.get('user_crop_id')

    print('here now')
    database.add_task(user_id, user_crop_id, task_name, task_date)

    return flask.jsonify({"success": True})

@app.route('/deleteCrop/<user_crop_id>', methods = ['POST'])
def delete_crop(user_crop_id):
    database.delete_template(user_crop_id)
    return redirect('/homepage')