#-----------------------------------------------------------------------
# Wildflower Farm App
#-----------------------------------------------------------------------

import time
import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates')

#-----------------------------------------------------------------------

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html',
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectFamily', methods=['GET'])
def search_crops():
    cropname = flask.request.args.get('crop_name')
    if cropname == None:
        cropname = ""
    
    crops = database.get_crop_info(cropname, 'family')
    seen_families = set()
    unique_families = []
    for crop in crops:
        if crop['family'] not in seen_families:
            unique_families.append(crop)
            seen_families.add(crop['family'])


    html_code = flask.render_template('selectFamily.html',
                                      crops = unique_families,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

from urllib.parse import unquote

@app.route('/selectSpecies/<family>', methods=['GET'])
def show_species(family):
    crops = database.get_crop_info(family, 'family')

    seen_species = set()
    unique_species = []
    for crop in crops:
        if crop['species'] not in seen_species:
            unique_species.append(crop)
            seen_species.add(crop['species'])


    html_code = flask.render_template('selectSpecies.html', 
                                      family=family,
                                      crops = unique_species,
                                      current_time = get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectVariety/<species>', methods=['GET'])
def show_variety(species):
    crops = database.get_crop_info(species, 'species')
    print(crops)
    seen_variety = set()
    unique_variety = []
    for crop in crops:
        if crop['variety'] not in seen_variety:
            unique_variety.append(crop)
            seen_variety.add(crop['variety'])
    
    html_code = flask.render_template(
        'selectVariety.html',
        species=species,
        crops=unique_variety,
        current_time=get_current_time()
    )
    
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/selectType/<crop_type>', methods=['GET'])
def show_type(crop_type):
    crops = database.get_crop_info(crop_type, 'variety')

    html_code = flask.render_template(
        'selectType.html',
        crop_type=crop_type,
        crops=crops,  
        current_time=get_current_time()
    )

    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/showcrop/<crop_name>', methods=['GET'])
def show_crop(crop_name):
    crops = database.get_crop_info(crop_name, 'crop_type')

    html_code = flask.render_template('showcrop.html',
                                      crop_name=crop_name,
                                      crop_infos=crops,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/createvariety/<species>', methods=['GET'])
def create_variety(species):
    crops = database.get_crop_info(species, 'species')
    print(crops)
    html_code = flask.render_template('createvariety.html',
                                      species=species,
                                      crop_info=crops[0],
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/addvariety/<species>', methods=['POST'])
def add_variety(species):
    crops = database.get_crop_info(species, 'species')
    variety = flask.request.form.get('variety')
    family = flask.request.form.get('family')
    seed_spacing_inches = flask.request.form.get('seed_spacing_inches')
    row_spacing_inches = flask.request.form.get('row_spacing_inches')
    seed_spacing_harvest = flask.request.form.get('seed_spacing_harvest')
    row_spacing_harvest = flask.request.form.get('row_spacing_harvest')
    days_to_transplantation = flask.request.form.get('days_to_transplantation')
    days_to_seed_maturity = flask.request.form.get('days_to_seed_maturity')
    days_to_direct_sow = flask.request.form.get('days_to_direct_sow')
    days_to_harvest = flask.request.form.get('days_to_harvest')
    days_to_seed_harvest = flask.request.form.get('days_to_seed_harvest')
    indoor_seed_starting_date= flask.request.form.get('indoor_seed_starting_date')
    transplanting_date = flask.request.form.get('transplanting_date')
    direct_sow_date = flask.request.form.get('direct_sow_date')
    harvest_date = flask.request.form.get('harvest_date')
    seed_harvest_date = flask.request.form.get('seed_harvest_date')
    frost_sensitivity_rating = flask.request.form.get('frost_sensitivity_rating')

    crop_info = {'latin_name':crops[0]['latin_name'], 'variety':variety, 'template':False,
                         'crop_type':crops[0]['crop_type'], 
                         'family':family,
                         'species':species,
                         'seed_spacing_inches':seed_spacing_inches, 'row_spacing_inches':row_spacing_inches,
                         'seed_spacing_harvest':seed_spacing_harvest, 'row_spacing_harvest':row_spacing_harvest,
                         'days_to_transplantation':days_to_transplantation, 'days_to_seed_maturity':days_to_seed_maturity,
                         'days_to_direct_sow':days_to_direct_sow, 'days_to_harvest':days_to_harvest,
                         'days_to_seed_harvest':days_to_seed_harvest, 'indoor_seed_starting_date':indoor_seed_starting_date,
                         'transplanting_date':transplanting_date, 'direct_sow_date':direct_sow_date, 'harvest_date':harvest_date,
                         'seed_harvest_date':seed_harvest_date, 'frost_sensitivity_rating':frost_sensitivity_rating}
    database.add_crop(crop_info)
    return index()
