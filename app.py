#-----------------------------------------------------------------------
# Wildflower Farm App
#-----------------------------------------------------------------------

import time
import flask
import database

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='templates')

#-----------------------------------------------------------------------

def get_ampm():
    if time.strftime('%p') == "AM":
        return 'morning'
    return 'afternoon'

def get_current_time():
    return time.asctime(time.localtime())

#-----------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    html_code = flask.render_template('index.html',
                                      ampm=get_ampm(),
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/searchcrops', methods=['GET'])
def search_crops():
    html_code = flask.render_template('searchcrops.html',
                                      ampm=get_ampm(),
                                      current_time=get_current_time())
    response = flask.make_response(html_code)
    return response

#-----------------------------------------------------------------------

@app.route('/searchresults', methods=['GET'])
def search_results():
    crop_name = flask.request.args.get('crop_name')
    if crop_name is None:
        crop_name = ''
    crop_name = crop_name.strip()

    crop_infos = database.get_crop_info(crop_name)

    html_code = flask.render_template('searchresults.html',
                                      ampm=get_ampm(),
                                      current_time=get_current_time(),
                                      crop_infos=crop_infos)
    response = flask.make_response(html_code)
    return response

        