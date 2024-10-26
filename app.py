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

@app.route('/searchcrops', methods=['GET'])
def search_crops():
    cropname = flask.request.args.get('crop_name')
    if cropname == None:
        cropname = ""
    
    crops = database.get_crop_info(cropname)
    html_code = flask.render_template('searchcrops.html',
                                      crops = crops,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/showcrop/<crop_name>', methods=['GET'])
def show_crop(crop_name):
    crops = database.get_crop_info(crop_name)
    html_code = flask.render_template('showcrop.html',
                                      crop_name=crop_name,
                                      crop_infos=crops,
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/createvariety/<crop_name>', methods=['GET'])
def create_variety(crop_name):
    crops = database.get_crop_info(crop_name)
    html_code = flask.render_template('createvariety.html',
                                      crop_name=crop_name,
                                      crop_info=crops[0],
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/addvariety/<crop_name>', methods=['POST'])
def add_variety(crop_name):
    variety = flask.request.args.get('variety')
    crops = database.get_crop_info(crop_name)
    seed_spacing_inches = flask.request.args.get('seed_spacing_inches')
    row_spacing_inches = flask.request.args.get('row_spacing_inches')
    seed_spacing_harvest = flask.request.args.get('seed_spacing_harvest')
    row_spacing_harvest = flask.request.args.get('row_spacing_harvest')
    days_to_transplantation = flask.request.args.get('days_to_transplantation')
    days_to_seed_maturity = flask.request.args.get('days_to_seed_maturity')
    days_to_direct_sow = flask.request.args.get('days_to_direct_sow')
    days_to_harvest = flask.request.args.get('days_to_harvest')
    days_to_seed_harvest = flask.request.args.get('days_to_seed_harvest')
    indoor_seed_starting_date= flask.request.args.get('indoor_seed_starting_date')
    transplanting_date = flask.request.args.get('transplanting_date')
    direct_sow_date = flask.request.args.get('direct_sow_date')
    harvest_date = flask.request.args.get('harvest_date')
    seed_harvest_date = flask.request.args.get('seed_harvest_date')
    frost_sensitivity_rating = flask.request.args.get('frost_sensitivity_rating')

    crop_info = {'latin_name':crops[0]['latin_name'], 'variety':variety, 'template':False,
                         'type':crop_name, 'seed_spacing_inches':seed_spacing_inches, 'row_spacing_inches':row_spacing_inches,
                         'seed_spacing_harvest':seed_spacing_harvest, 'row_spacing_harvest':row_spacing_harvest,
                         'days_to_transplantation':days_to_transplantation, 'days_to_seed_maturity':days_to_seed_maturity,
                         'days_to_direct_sow':days_to_direct_sow, 'days_to_harvest':days_to_harvest,
                         'days_to_seed_harvest':days_to_seed_harvest, 'indoor_seed_starting_date':indoor_seed_starting_date,
                         'transplanting_date':transplanting_date, 'direct_sow_date':direct_sow_date, 'harvest_date':harvest_date,
                         'seed_harvest_date':seed_harvest_date, 'frost_sensitivity_rating':frost_sensitivity_rating}
    database.add_crop(crop_info)
    return index()
