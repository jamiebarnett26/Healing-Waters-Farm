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
    #user_id = flask.request.cookies.get('user_id')
    #if not user_id:
     #   return flask.redirect('/login')
    user_id = flask.request.cookies.get('user_id')
    user_crops = database.get_user_crops(user_id)
    user_crop_infos = []
    all_todos = []
    variety_id = []

    for i, user_crop in enumerate(user_crops):
        full_crop_info = database.full_crop_info(user_crop['crop_info_id'])
        if full_crop_info == -1:
            break
        user_crop_infos.append(full_crop_info)

        variety_name = user_crop_infos[i]['variety_name']
        variety_dict = database.search_field_name("variety", variety_name)
        variety_id.append(variety_dict[0]['variety_id'])
        
        todos = getWeeklyTasks(user_crop, full_crop_info['frost_sensitivity_rating'])
        all_todos.append(todos)
    
    crops_with_todos = zip(user_crop_infos, all_todos, variety_id)
    
    return crops_with_todos

def getWeeklyTasks(user_crop, frost_rating):
    today = datetime.date.today()
    enddate = today + datetime.timedelta(days=7)
    todos = []
    if user_crop['indoor_seed_starting_date'] <= enddate:
        todos.append({"task": "Start indoor seeding", "date": user_crop['indoor_seed_starting_date'], "done": False})
    if user_crop['transplanting_date'] <= enddate:
        todos.append({"task": "Transplant plants outdoors", "date": user_crop['transplanting_date'], "done": False})
    if user_crop['direct_sow_date'] <= enddate:
        todos.append({"task": "Direct sowing", "date": user_crop['direct_sow_date'], "done": False})
    if user_crop['harvest_date'] <= enddate:
        todos.append({"task": "Prepare for harvest", "date": user_crop['harvest_date'], "done": False})
    if user_crop['seed_harvest_date'] <= enddate:
        todos.append({"task": "Prepare for seed harvest", "date": user_crop['seed_harvest_date'], "done": False})
    if frost_rating > 1 and inFrost():
        todos.append({"task": "This plant is frost-sensitive and you are in a frost!", "date": today, "done": False})

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
    
    html_code = flask.render_template('showcrop.html',
                                      crop_info_id=crop_infos[0]['crop_info_id'],
                                      admin=admin,
                                      crop_infos=full_crop_infos,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

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
