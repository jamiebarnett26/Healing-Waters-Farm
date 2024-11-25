
from top import app, oauth
import flask
from flask import redirect
import database
import time
import json
import sys

#-----------------------------------------------------------------------

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------
# METHODS FOR HOMEPAGE
#-----------------------------------------------------------------------
@app.route('/weather', methods=['GET'])
def load_weather():
    html_code = flask.render_template('homepage/boxes_w_info.html')
    response = flask.make_response(html_code)
    return response

@app.route('/cropCards', methods=['GET'])
def load_cropcards():
    print("IN SERVER INITIAL")
    return flask.send_file('templates/homepage/cropcards.html')

@app.route('/footer', methods=['GET'])
def load_footer():
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('footer.html', admin=admin)
    response = flask.make_response(html_code)
    return response


#-----------------------------------------------------------------------
# METHODS FOR SERIES OF CROP SELECTION
#-----------------------------------------------------------------------
@app.route('/selectFamily', methods=['GET'])
def search_crops():
    return flask.send_file('templates/addCrop/selectFamily.html')
#--------------------------
@app.route('/showFamily', methods=['GET'])
def show_family():
    family = flask.request.args.get('family', '')
    families = database.search_field_name('family', family)
    json_doc = json.dumps(families)
        
    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'
    return response
#--------------------------
@app.route('/showSpecies', methods=['GET'])
def show_species():
    #admin = flask.request.cookies.get('admin') == 'true'

    familyId = flask.request.args.get('family', '')
    species = database.species_from_family(familyId)
    json_doc = json.dumps(species)

    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'
    return response
#--------------------------
@app.route('/showVariety', methods=['GET'])
def show_variety():
    #admin = flask.request.cookies.get('admin') == 'true'

    speciesId = flask.request.args.get('species', '')
    species = database.variety_from_species(speciesId)
    json_doc = json.dumps(species)

    response = flask.make_response(json_doc)
    response.headers['Content-Type'] = 'application/json'
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

@app.route('/editfamily/<family_id>', methods=['GET'])
def edit_family(family_id):
    family = database.search_field_id('family', family_id)
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('editfamily.html',
                                      admin=admin,
                                      family=family[0],
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

@app.route('/posteditfamily/<family_id>', methods=['POST'])
def post_edit_family(family_id):
    family_name = flask.request.form.get('family_name')
    family = {'family_name':family_name}
    database.edit_family(family_id, family)
    return select_family()

#-----------------------------------------------------------------------

@app.route('/editspecies/<species_id>', methods=['GET'])
def edit_species(species_id):
    species = database.search_field_id('species', species_id)
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('editspecies.html',
                                      admin=admin,
                                      species=species[0],
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

@app.route('/posteditspecies/<species_id>', methods=['POST'])
def post_edit_species(species_id):
    species_name = flask.request.form.get('species_name')
    latin_name = flask.request.form.get('latin_name')
    species = {'species_name':species_name, 'latin_name':latin_name}
    database.edit_species(species_id, species)
    return select_family()

#-----------------------------------------------------------------------

@app.route('/editvariety/<variety_id>', methods=['GET'])
def edit_variety(variety_id):
    variety = database.search_field_id('variety', variety_id)
    admin = flask.request.cookies.get('admin') == 'true'
    html_code = flask.render_template('editvariety.html',
                                      admin=admin,
                                      variety=variety[0],
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response
    

@app.route('/posteditvariety/<variety_id>', methods=['POST'])
def post_edit_variety(variety_id):
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

    variety = {'variety_name':variety_name}

    crop_info = {'crop_type':crop_type, 'template':False, 'plant_spacing_harvest':plant_spacing_harvest,
                 'plant_spacing_seed':plant_spacing_seed, 'row_spacing_harvest':row_spacing_harvest,
                 'row_spacing_seed':row_spacing_seed, 'days_to_maturity_harvest':days_to_maturity_harvest,
                 'days_to_maturity_seed':days_to_maturity_seed, 'days_to_transplantation':days_to_transplantation,
                 'days_to_direct_sow':days_to_direct_sow, 'days_to_harvest':days_to_harvest, 'days_to_seed_harvest':days_to_seed_harvest,
                 'frost_sensitivity_rating':frost_sensitivity_rating
                 }

    database.edit_variety(variety_id, variety, crop_info)
    return select_family()

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

@app.route('/addfamily', methods=['POST'])
def add_family():
    family_name = flask.request.form.get('family_name')
    family = {'family_name':family_name}
    database.add_family(family)
    return select_family()

@app.route('/addspecies/<family_id>', methods=['POST'])
def add_species(family_id):
    species_name = flask.request.form.get('species_name')
    latin_name = flask.request.form.get('latin_name')
    species = {'family_id':family_id, 'species_name':species_name, 'latin_name':latin_name}
    database.add_species(species)
    return select_family()


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
    return select_family()
#-----------------------------------------------------------------------
# functionality to delete
@app.route('/deletefamily/<family_id>')
def delete_family(family_id):
    database.delete_family(family_id)
    return select_family()

@app.route('/deletespecies/<species_id>')
def delete_species(species_id):
    database.delete_species(species_id)
    return select_family()

@app.route('/deletevariety/<variety_id>')
def delete_variety(variety_id):
    database.delete_variety(variety_id)
    return select_family()

