#-----------------------------------------------------------------------
# Wildflower Farm App
#-----------------------------------------------------------------------

import time
import flask 
import database
import datetime

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_client import OAuth
from top import app
import json
import auth
import crop_infos
import sys

#-----------------------------------------------------------------------

auth = flask.Blueprint('auth', __name__)

#-----------------------------------------------------------------------

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------
# Start of app, outputs login page
@app.route('/', methods=['GET'])
def index():
    user_id = flask.request.cookies.get('user_id')

    # Instead of redirecting immediately, consider rendering a welcome page.
    if user_id:
        user = database.get_user(user_id, 'user_id')
        if user:
            return flask.redirect('/login')

    # Show a simple welcome or landing page if no user_id is found.
    return flask.redirect('/login')

#-----------------------------------------------------------------------
# Currently not in use - loads manual login page
@app.route('/manual_login')
def manual_login():
    html_code = flask.render_template('manual_login.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
# Helper function, returns crop to do list for cards
def getCardInfo():
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



@app.route('/delete_template', methods = ['POST'])
def deleteTemplate():
    user_crop_id = flask.request.args.get('cropid')
    try: 
        database.delete_template(user_crop_id)
        return flask.jsonify({'success': True, 'message': 'Template deleted successfully'})
    except Exception as e:
        return flask.jsonify({'success': False, 'message': str(e)}), 500




@app.route('/edit_task', methods = ['POST'])
def editTask():
    user_id = flask.request.cookies.get('user_id')
    data = flask.request.get_json()
    user_crop_id = data.get('user_crop_id')
    date_field = data.get('date_field')
    new_date = data.get('new_date')
    try: 
        database.edit_user_tasks(user_id, user_crop_id, date_field, new_date)
        return flask.jsonify({'success': True, 'message': 'Date updated successfully'})
    except Exception as e:
        return flask.jsonify({'success': False, 'message': str(e)}), 500

@app.route('/add_task', methods = ['POST'])
def addTask():
    user_id = flask.request.cookies.get('user_id')
    data = flask.request.get_json()
    user_crop_id = data.get('user_crop_id')
    task_name = data.get('new_task')
    task_date = data.get('new_date')
    try: 
        database.add_task(user_id, user_crop_id, task_name, task_date)
        return flask.jsonify({'success': True, 'message': 'Task added successfully'})
    except Exception as e:
        return flask.jsonify({'success': False, 'message': str(e)}), 500

def getWeeklyTasks(user_crop, frost_rating):
    today = datetime.date.today()
    enddate = today + datetime.timedelta(days=7)
    todos = []
    
    if user_crop['indoor_seed_starting_date'] is not None and user_crop['indoor_seed_starting_date'] <= enddate:
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "Start indoor seeding", "date": user_crop['indoor_seed_starting_date'], "done": False})
    if user_crop['transplanting_date'] is not None and  user_crop['transplanting_date'] <= enddate:
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "Transplant plants outdoors", "date": user_crop['transplanting_date'], "done": False})
    if user_crop['direct_sow_date'] is not None and user_crop['direct_sow_date'] <= enddate:
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "Direct sowing", "date": user_crop['direct_sow_date'], "done": False})
    if user_crop['harvest_date'] is not None and user_crop['harvest_date'] <= enddate:
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "Prepare for harvest", "date": user_crop['harvest_date'], "done": False})
    if user_crop['seed_harvest_date'] is not None and user_crop['seed_harvest_date'] <= enddate:
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "Prepare for seed harvest", "date": user_crop['seed_harvest_date'], "done": False})
    if frost_rating is not None and frost_rating > 1 and inFrost():
        todos.append({"user_crop_id":user_crop['user_crop_id'], "task": "This plant is frost-sensitive and you are in a frost!", "date": today, "done": False})

    return todos

def inFrost():
    today = datetime.datetime.today()
    
    # Create datetime objects for October 20 and April 21 of the current year
    oct_20 = datetime.datetime(today.year, 10, 20)
    apr_21 = datetime.datetime(today.year+1, 4, 21)
    
    print(apr_21, file=sys.stderr)
    print(oct_20, file=sys.stderr)
    # Check if today is between the two dates
    return oct_20 <= today <= apr_21



#-----------------------------------------------------------------------
# Loads main page of app
@app.route('/homepage', methods = ["GET"])
def homepage():
    user_id = flask.request.cookies.get('user_id')
    admin = flask.request.cookies.get('admin') == 'true'
    app.logger.info(admin)

    if not user_id:
        return flask.redirect('/login')
    user = database.get_user(user_id, 'user_id')
    if not user:
        return flask.redirect('/login')
     
    user_name = user.first_name + " " + user.last_name

    crops_with_todos = getCardInfo()
    html_code = flask.render_template('homepage/homepage.html',
                                      user_name=user_name,
                                      admin=admin,
                                      crops_with_todos=crops_with_todos)
    response = flask.make_response(html_code)
    return response

@app.route('/testingnewcropinfo', methods = ['GET'])
def new_show_crop():
    return flask.send_file('templates/newcropinfo.html')

#-----------------------------------------------------------------------
# @app.route('/showcrop/<int:crop_info_id>')
# def showcrop(crop_info_id):
#     crop_infos = [database.full_crop_info(crop_info_id)]  # Retrieve specific crop info
#     crops_with_todos = getCardInfo()  # Get crop and task details
#     return flask.render_template('showcrop.html', crop_infos=crop_infos, crops_with_todos=crops_with_todos)

#-----------------------------------------------------------------------
# Route end points for login.


#-----------------------------------------------------------------------
# Admin functionality of seeing all profiles, loads profile_list.html
@app.route('/profile_list', methods=['GET'])
def profile_list():
    admin = flask.request.cookies.get('admin') == 'true'
    profiles = database.get_profiles()
    html_code = flask.render_template('profile_list.html',
                                      admin=admin,
                                      profiles=profiles,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

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
    title = flask.request.form.get('title')
    text = flask.request.form.get('text')
    question = {'user_id':user_id, 'title':title, 'text':text, 'status':'Unresolved'}
    database.add_question(question)
    return community()

    
#-----------------------------------------------------------------------

@app.route('/editquestion/<question_id>', methods=['POST'])
def post_edit_question(question_id):
    title = flask.request.form.get('title')
    text  = flask.request.form.get('text')
    question = {'title':title, 'text':text}
    database.edit_question(question_id, question)
    return community()

#-----------------------------------------------------------------------
# functionality to delete
@app.route('/deletequestion/<question_id>', methods=['POST'])
def delete_question(question_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_question(user_id, question_id)
    return community()


#-----------------------------------------------------------------------

@app.route('/addreply/<question_id>', methods=['POST'])
def add_reply(question_id):
    user_id = flask.request.cookies.get('user_id')
    text = flask.request.form.get('text')
    reply = {'question_id':question_id,'user_id':user_id, 'text':text}
    database.add_reply(reply)
    return community()

#-----------------------------------------------------------------------

@app.route('/editreply/<reply_id>', methods=['POST'])
def post_edit_reply(reply_id):
    text  = flask.request.form.get('text')
    reply = {'text':text}
    database.edit_reply(reply_id, reply)
    return community()

#-----------------------------------------------------------------------
# functionality to delete
@app.route('/deletereply/<reply_id>', methods=['POST'])
def delete_reply(reply_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_reply(user_id, reply_id)
    return community()

#-----------------------------------------------------------------------

@app.route('/addannouncement/', methods=['POST'])
def add_announcement():
    user_id = flask.request.cookies.get('user_id')
    text = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'user_id':user_id, 'text':text, 'title':title}
    database.add_announcement(announcement)
    return community()
    
#-----------------------------------------------------------------------

@app.route('/editannouncement/<announcement_id>', methods=['POST'])
def post_edit_announcement(announcement_id):
    text  = flask.request.form.get('text')
    title = flask.request.form.get('title')
    announcement = {'text':text, 'title':title}
    database.edit_announcement(announcement_id, announcement)
    return community()

#-----------------------------------------------------------------------
# functionality to delete
@app.route('/deleteannouncement/<announcement_id>', methods=['POST'])
def delete_announcement(announcement_id):
    user_id = flask.request.cookies.get('user_id')
    database.delete_announcement(user_id, announcement_id)
    return community()

# helper method to get varieties and latin names as lists for user crops
def get_crop_varieties_and_latin(user_id):
    user_crops = database.get_user_crops(user_id)

    crop_data = []
    for user_crop in user_crops:
        crop_info = database.full_crop_info(user_crop['crop_info_id'])
        variety_id = crop_info['variety_id']  # Assuming this field exists in your database schema
        variety_name = crop_info['variety_name']
        latin_name = crop_info['latin_name']
        crop_data.append((variety_id, variety_name, latin_name))

    return crop_data



#-----------------------------------------------------------------------
# Rdirects to account.html
@app.route('/account', methods=['GET'])
def oldIndex():
    html_code = flask.render_template('account.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
# Request from homepage by selecting a crop, directs to indv CropPage_task.html
@app.route('/cropPage/<variety_name>', methods = ["GET"])
def cropPage(variety_name):
    html_code = flask.render_template('indvCropPage/cropPage_tasks.html', variety_name = variety_name)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
# Loads the My Crops page (Showcasing all crops)
@app.route('/showcrop/<variety_id>', methods=['GET'])
def show_crop(variety_id):
    admin = flask.request.cookies.get('admin') == 'true'
    crop_infos = database.crop_info_from_variety(variety_id)
    full_crop_infos = []
    for crop_info in crop_infos:
        full_crop_info = database.full_crop_info(crop_info['crop_info_id'])
        full_crop_infos.append(full_crop_info)

    app.logger.info(variety_id)
    app.logger.info(database.species_from_variety(variety_id))
    species_id = database.species_from_variety(variety_id).species_id
    app.logger.info(species_id)
    html_code = flask.render_template('showcrop.html',
                                      crop_info_id=crop_infos[0]['crop_info_id'],
                                      species_id=species_id,
                                      crop_infos=full_crop_infos)
    response = flask.make_response(html_code)
    return response


#-----------------------------------------------------------------------

# @app.route('/selectCropSpecification', methods=['GET'])
# def show_species():
#     family = flask.request.args.get('family', '')
#     families = database.search_field_name('family', family)

#     json_doc = json.dumps(families)
#     response = flask.make_response(json_doc)
#     response.headers['Content-Type'] = 'application/json'
#     return response

# #-----------------------------------------------------------------------

# @app.route('/selectVariety/<species_id>', methods=['GET'])
# def show_variety(species_id):
#     admin = flask.request.cookies.get('admin') == 'true'
#     varieties = database.variety_from_species(species_id)
    
#     html_code = flask.render_template(
#         'addCrop/selectVariety.html',
#         varieties=varieties,
#         species_id=species_id,
#         admin=admin,
#         current_time=get_current_time()
#     )
    
#     response = flask.make_response(html_code)
#     return response

# #-----------------------------------------------------------------------

# @app.route('/createfamily', methods=['GET'])
# def create_family():
#     admin = flask.request.cookies.get('admin') == 'true'
#     html_code = flask.render_template('createfamily.html',
#                                       admin=admin,
#                                       crop_infos=full_crop_infos,
#                                       current_time=get_current_time())
#     response = flask.make_response(html_code)
#     return response

#-----------------------------------------------------------------------


@app.route('/addusercrop/<crop_info_id>')
def add_user_crop(crop_info_id):
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    crop_info = database.search_field_id('crop_info', crop_info_id)[0]

    date1 = datetime.datetime.now()
    date2 = date1 + datetime.timedelta(days=crop_info['days_to_transplantation'])
    date3 = date2 + datetime.timedelta(crop_info['days_to_direct_sow'])
    date4 = date3 + datetime.timedelta(crop_info['days_to_harvest'])
    date5 = date3 + datetime.timedelta(crop_info['days_to_seed_harvest'])
    
    
    user_crop = {
        'user_id': user_id,
        'crop_info_id': crop_info_id,
        'indoor_seed_starting_date': date1,
        'transplanting_date': date2,
        'direct_sow_date': date3,
        'harvest_date': date4,
        'seed_harvest_date': date5
    }

    database.add_user_crop(user_crop)

    return homepage()

#-----------------------------------------------------------------------

@app.route('/showusercrops', methods=['GET'])
def my_crops():
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    user_crops = database.get_user_crops(user_id)
    user_crop_infos = []
    for user_crop in user_crops:
        user_crop_info = database.full_crop_info(user_crop['crop_info_id'])
        user_crop_infos.append(user_crop_info)
    return flask.render_template('showusercrops.html', crops=user_crop_infos)


#-----------------------------------------------------------------------

@app.route('/calendar')
def calendar():
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('calendar.html', admin=admin)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/serviceWorker.js')
def serve_sw():
    return app.send_static_file('serviceWorker.js')

#-----------------------------------------------------------------------
