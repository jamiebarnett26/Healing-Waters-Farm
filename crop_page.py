from top import app, oauth
import flask
from flask import redirect
import database
import time
import json
import sys

def get_current_time():
    return time.asctime(time.localtime())

@app.route('/getTasks', methods=['GET'])
def get_tasks():
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')

    user_crops = database.get_user_crops(user_id)
    if user_crops is None:
        app.logger.error("No crops found for user_id: %s", user_id)
        return []  # Return an empty list if no crops exist.

    user_crop_infos = []
    all_todos = []
    variety_id = []

    current_crop = database.get_user_crops

    for i, user_crop in enumerate(user_crops):
        # Safely fetch full_crop_info
        full_crop_info = database.full_crop_info(user_crop['crop_info_id'])
        if full_crop_info is None:
            app.logger.error("No full crop info found for crop_info_id: %s", user_crop['crop_info_id'])
            continue  # Skip this crop if no info is found.

        user_crop_infos.append(full_crop_info)
        app.logger.info("Added crop info: %s", full_crop_info)

        # Safely fetch variety_dict
        variety_name = full_crop_info.get('variety_name')  # Use .get() for safe access
        if not variety_name:
            app.logger.error("Variety name missing in crop info: %s", full_crop_info)
            continue

        variety_dict = database.search_field_name("variety", variety_name)
        if not variety_dict:
            app.logger.error("No variety found for variety_name: %s", variety_name)
            continue

        variety_id.append(variety_dict[0].get('variety_id', None))
        if variety_id[-1] is None:
            app.logger.error("Variety ID missing for variety_name: %s", variety_name)
            continue

        # Safely get todos
        todos = getWeeklyTasks(user_crop, full_crop_info.get('frost_sensitivity_rating', 0))
        if todos is None:
            todos = []  # Default to an empty list if no tasks found.

        database.get_user_added_tasks(user_crop.get('user_crop_id'), todos)
        all_todos.append(todos)

    # Ensure all lists have the same length
    if len(user_crop_infos) != len(all_todos) or len(user_crop_infos) != len(variety_id):
        app.logger.error("Mismatch in lengths of user_crop_infos, all_todos, and variety_id")

    crops_with_todos = zip(user_crop_infos, all_todos, variety_id)
    return crops_with_todos