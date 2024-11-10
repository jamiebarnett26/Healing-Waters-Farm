#-----------------------------------------------------------------------
# Wildflower Farm App
#-----------------------------------------------------------------------

import time
import flask
import database
from datetime import datetime

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates')

#-----------------------------------------------------------------------

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/oldIndex', methods=['GET'])
def getHomePage():
    html_code = flask.render_template('oldIndex.html',
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response


#-----------------------------------------------------------------------
def getCardInfo():
    user_crops = database.get_user_crops(1)
    user_crop_infos = []
    all_todos = []
    for user_crop in user_crops:
        user_crop_infos.append(database.full_crop_info(user_crop['crop_info_id']))

        todos = [
            {"task": "Start indoor seeding", "date": user_crop['indoor_seed_starting_date'], "done": False},
            {"task": "Transplant plants outdoors", "date": user_crop['transplanting_date'], "done": False},
            {"task": "Direct sowing", "date": user_crop['direct_sow_date'], "done": False},
            {"task": "Prepare for harvest", "date": user_crop['harvest_date'], "done": False}
        ]
        all_todos.append(todos)
    
    crops_with_todos = zip(user_crop_infos, all_todos)
    
    return crops_with_todos

#-----------------------------------------------------------------------

@app.route('/homepage', methods = ["GET"])
def goHomepage():
    crops_with_todos = getCardInfo()
    html_code = flask.render_template('homepage/homepage.html', crops_with_todos=crops_with_todos)
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/testpage', methods = ["GET"])
def testpage():
    html_code = flask.render_template('homepage/testpage.html')
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/selectFamily', methods=['GET'])
def search_crops():
    family = flask.request.args.get('family')
    if family == None:
        family = ""
    
    families= database.search_field_name('family', family)
    html_code = flask.render_template('selectFamily.html',
                                      families=families,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectSpecies/<family_id>', methods=['GET'])
def show_species(family_id):
    species = database.species_from_family(family_id)

    html_code = flask.render_template('selectSpecies.html', 
                                      species=species,
                                      family_id=family_id,
                                      current_time = get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectVariety/<species_id>', methods=['GET'])
def show_variety(species_id):
    varieties = database.variety_from_species(species_id)
    
    html_code = flask.render_template(
        'selectVariety.html',
        varieties=varieties,
        species_id=species_id,
        current_time=get_current_time()
    )
    
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/showcrop/<variety_id>', methods=['GET'])
def show_crop(variety_id):
    crop_infos = database.crop_info_from_variety(variety_id)
    full_crop_infos = []
    for crop_info in crop_infos:
        full_crop_info = database.full_crop_info(crop_info['crop_info_id'])
        full_crop_infos.append(full_crop_info)
    html_code = flask.render_template('showcrop.html',
                                      crop_info_id=crop_info['crop_info_id'],
                                      crop_infos=full_crop_infos,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------
@app.route('/createfamily', methods=['GET'])
def create_family():
    html_code = flask.render_template('createfamily.html',
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

#-----------------------------------------------------------------------

@app.route('/addfamily', methods=['POST'])
def add_family():
    family_name = flask.request.form.get('family_name')
    family = {'family_name':family_name}
    database.add_family(family)
    return index()

#-----------------------------------------------------------------------

@app.route('/deletefamily/<family_id>')
def delete_family(family_id):
    database.delete_family(family_id)
    return index()

#-----------------------------------------------------------------------

@app.route('/deletespecies/<species_id>')
def delete_species(species_id):
    database.delete_species(species_id)
    return index()

#-----------------------------------------------------------------------

@app.route('/deletevariety/<variety_id>')
def delete_variety(variety_id):
    database.delete_variety(variety_id)
    return index()


#-----------------------------------------------------------------------
@app.route('/createspecies/<family_id>', methods=['GET'])
def create_species(family_id):
    html_code = flask.render_template('createspecies.html',
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
    return index()


#-----------------------------------------------------------------------
@app.route('/createvariety/<species_id>', methods=['GET'])
def create_variety(species_id):
    template_crop_id = database.get_template_crop(species_id)
    if template_crop_id == -1:
        family_table = database.family_from_species(species_id)
        species_table = database.search_field_id('species', species_id)
        print(family_table.family_name)
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
    return index()

#-----------------------------------------------------------------------

@app.route('/addusercrop/<crop_info_id>')
def add_user_crop(crop_info_id):

    indoor_seed_starting_date = datetime.now()
    
    user_crop = {
        'user_id': 1,
        'crop_info_id': crop_info_id,
        'indoor_seed_starting_date': indoor_seed_starting_date,
        'transplanting_date': None,
        'direct_sow_date': None,
        'harvest_date': None,
        'seed_harvest_date': None
    }

    database.add_user_crop(user_crop)

    return index()

#-----------------------------------------------------------------------

@app.route('/showusercrops')
def show_user_crop():
    user_crops = database.get_user_crops(1)
    user_crop_infos = []
    all_todos = []
    for user_crop in user_crops:
        user_crop_infos.append(database.full_crop_info(user_crop['crop_info_id']))

        todos = [
            {"task": "Start indoor seeding", "date": user_crop['indoor_seed_starting_date'], "done": False},
            {"task": "Transplant plants from indoor to outdoor", "date": user_crop['transplanting_date'], "done": False},
            {"task": "Direct sowing", "date": user_crop['direct_sow_date'], "done": False},
            {"task": "Prepare for harvest", "date": user_crop['harvest_date'], "done": False}
        ]
        all_todos.append(todos)
    
    crops_with_todos = zip(user_crop_infos, all_todos)

    html_code = flask.render_template('showusercrops.html',
                                      crops_with_todos=crops_with_todos,  
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/calendar')
def calendar():

    html_code = flask.render_template('calendar.html')
    response = flask.make_response(html_code)
    return response

