#-----------------------------------------------------------------------
# Wildflower Farm App
#-----------------------------------------------------------------------

import time
import flask 
import database
from datetime import datetime

from authlib.integrations.flask_client import OAuth
from authlib.integrations.flask_client import OAuth
from top import app
import auth
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
        user_crop_infos.append(database.full_crop_info(user_crop['crop_info_id']))
        
        variety_name = user_crop_infos[i]['variety_name']
        variety_dict = database.search_field_name("variety", variety_name)
        variety_id.append(variety_dict[0]['variety_id'])
        

        todos = [
            {"user_crop_id": user_crop['user_crop_id'], 
             "task": "Start indoor seeding", 
             "date": user_crop['indoor_seed_starting_date'], 
             "done": False},
            {"user_crop_id": user_crop['user_crop_id'], 
             "task": "Transplant plants outdoors", 
             "date": user_crop['transplanting_date'], 
             "done": False},
            {"user_crop_id": user_crop['user_crop_id'],
             "task": "Direct sowing", 
             "date": user_crop['direct_sow_date'], 
             "done": False},
            {"user_crop_id": user_crop['user_crop_id'],
             "task": "Prepare for harvest", 
             "date": user_crop['harvest_date'], 
             "done": False}
        ]
        database.get_user_added_tasks(user_crops[i]['user_crop_id'], todos)
        all_todos.append(todos)
    
    crops_with_todos = zip(user_crop_infos, all_todos, variety_id)
    
    return crops_with_todos

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
                                      crops_with_todos=crops_with_todos,)
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
    
# @app.route('/home', methods=['GET'])
# def home():
#     user_id = flask.request.cookies.get('user_id')
#     admin = flask.request.cookies.get('admin') == 'true'
#     app.logger.info(admin)

#     if not user_id:
#         return flask.redirect('/login')
#     user = database.get_user(user_id, 'user_id')
#     if not user:
#         return flask.redirect('/login')
     
#     user_name = user.first_name + " " + user.last_name
   
#     html_code = flask.render_template('home.html',
#                                       user_name=user_name,
#                                       admin=admin,
#                                       current_time=get_current_time())
#     response = flask.make_response(html_code)
#     return response


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
# Request from homepage by adding crop card, directs to selectFamily.html
@app.route('/selectFamily', methods=['GET'])
def search_crops():
    admin = flask.request.cookies.get('admin') == 'true'
    family = flask.request.args.get('family')
    if family == None:
        family = ""
    
    families= database.search_field_name('family', family)
    html_code = flask.render_template('addCrop/selectFamily.html',
                                      families=families,
                                      admin = admin,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectSpecies/<family_id>', methods=['GET'])
def show_species(family_id):
    species = database.species_from_family(family_id)
    admin = flask.request.cookies.get('admin') == 'true'

    html_code = flask.render_template('addCrop/selectSpecies.html', 
                                      species=species,
                                      family_id=family_id,
                                      admin = admin,
                                      current_time = get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectVariety/<species_id>', methods=['GET'])
def show_variety(species_id):
    admin = flask.request.cookies.get('admin') == 'true'
    varieties = database.variety_from_species(species_id)
    
    html_code = flask.render_template(
        'addCrop/selectVariety.html',
        varieties=varieties,
        species_id=species_id,
        admin=admin,
        current_time=get_current_time()
    )
    
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/createfamily', methods=['GET'])
def create_family():
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('createfamily.html',
                                      admin=admin,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

#-----------------------------------------------------------------------

@app.route('/addfamily', methods=['POST'])
def add_family():
    family_name = flask.request.form.get('family_name')
    family = {'family_name':family_name}
    database.add_family(family)
    return homepage()

#-----------------------------------------------------------------------
# functionality to delete
@app.route('/deletefamily/<family_id>')
def delete_family(family_id):
    database.delete_family(family_id)
    return homepage()

@app.route('/deletespecies/<species_id>')
def delete_species(species_id):
    database.delete_species(species_id)
    return homepage()

@app.route('/deletevariety/<variety_id>')
def delete_variety(variety_id):
    database.delete_variety(variety_id)
    return homepage()

#-----------------------------------------------------------------------
@app.route('/createspecies/<family_id>', methods=['GET'])
def create_species(family_id):
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('createspecies.html',
                                      admin=admin,
                                      family_id=family_id,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

#-----------------------------------------------------------------------

@app.route('/addspecies/<family_id>', methods=['POST'])
def add_species(family_id):
    species_name = flask.request.form.get('species_name')
    latin_name = flask.request.form.get('latin_name')
    species = {'family_id':family_id, 'species_name':species_name, 'latin_name':latin_name}
    database.add_species(species)
    return homepage()


#-----------------------------------------------------------------------
@app.route('/createvariety/<species_id>', methods=['GET'])
def create_variety(species_id):
    admin = flask.request.cookies.get('admin') == 'true'
    template_crop_id = database.get_template_crop(species_id)
    if template_crop_id == -1:
        family_table = database.family_from_species(species_id)
        species_table = database.search_field_id('species', species_id)
        print(species_table)
        full_crop_info = {
            'family_name': family_table.family_name,
            'latin_name': species_table[0]['latin_name'],
            'variety_name': None,
            'crop_type': None,
            'template': None,
            'days_to_maturity': None,
            'plant_spacing_harvest': None,
            'plant_spacing_seed': None,
            'row_spacing_harvest': None,
            'row_spacing_seed': None, 
            'days_to_maturity_harvest': None,
            'days_to_maturity_seed': None,
            'days_to_transplantation': None,
            'days_to_direct_sow': None,
            'days_to_harvest': None,
            'days_to_seed_harvest': None,
            'frost_sensitivity_rating': None
        }
    else:
        full_crop_info = database.full_crop_info(template_crop_id)
    html_code = flask.render_template('createvariety.html',
                                      crop_info=full_crop_info,
                                      admin=admin,
                                      species_id=species_id,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/addvariety/<species_id>', methods=['POST'])
def add_variety(species_id):
    variety_name = flask.request.form.get('variety_name')
    crop_type = flask.request.form.get('crop_type_name')
    plant_spacing_harvest = flask.request.form.get('plant_spacing_harvest')
    row_spacing_harvest = flask.request.form.get('row_spacing_harvest')
    plant_spacing_seed = flask.request.form.get('plant_spacing_seed')
    row_spacing_seed = flask.request.form.get('row_spacing_seed')
    days_to_maturity_harvest = flask.request.form.get('days_to_maturity_harvest')
    days_to_maturity_seed = flask.request.form.get('days_to_maturity_seed')
    days_to_transplantation = flask.request.form.get('days_to_transplantation')
    days_to_direct_sow = flask.request.form.get('days_to_direct_sow')
    days_to_harvest = flask.request.form.get('days_to_harvest')
    days_to_seed_harvest = flask.request.form.get('days_to_seed_harvest')
    frost_sensitivity_rating = flask.request.form.get('frost_sensitivity_rating')

    variety = {'species_id':species_id, 'variety_name':variety_name}

    crop_info = {'crop_type':crop_type, 'template':False, 'plant_spacing_harvest':plant_spacing_harvest,
                 'plant_spacing_seed':plant_spacing_seed, 'row_spacing_harvest':row_spacing_harvest,
                 'row_spacing_seed':row_spacing_seed, 'days_to_maturity_harvest':days_to_maturity_harvest,
                 'days_to_maturity_seed':days_to_maturity_seed, 'days_to_transplantation':days_to_transplantation,
                 'days_to_direct_sow':days_to_direct_sow, 'days_to_harvest':days_to_harvest, 'days_to_seed_harvest':days_to_seed_harvest,
                 'frost_sensitivity_rating':frost_sensitivity_rating
                 }

    database.add_variety(variety, crop_info)
    return homepage()

@app.route('/addusercrop/<crop_info_id>')
def add_user_crop(crop_info_id):
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')

    indoor_seed_starting_date = datetime.now()
    
    user_crop = {
        'user_id': user_id,
        'crop_info_id': crop_info_id,
        'indoor_seed_starting_date': indoor_seed_starting_date,
        'transplanting_date': None,
        'direct_sow_date': None,
        'harvest_date': None,
        'seed_harvest_date': None
    }

    database.add_user_crop(user_crop)

    return homepage()

#-----------------------------------------------------------------------

@app.route('/showusercrops', methods=['GET'])
def my_crops():
    user_id = flask.request.cookies.get('user_id')
    if not user_id:
        return flask.redirect('/login')
    crops = get_crop_varieties_and_latin(user_id)
    return flask.render_template('showusercrops.html', crops=crops)


#-----------------------------------------------------------------------

@app.route('/calendar')
def calendar():
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('calendar.html', admin=admin)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

#@app.route('/manifest.json')
#def serve_manifest():
#    return flask.send_file('manifest.json')
    #, mimetype='application/manifest+json'

#-----------------------------------------------------------------------

@app.route('/serviceWorker.js')
def serve_sw():
    return app.send_static_file('serviceWorker.js')

#-----------------------------------------------------------------------
