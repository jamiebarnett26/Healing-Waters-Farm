#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
import dotenv

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()

class Crop_Info (Base):
    __tablename__ = 'crop_information'
    crop_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    template = sqlalchemy.Column(sqlalchemy.Boolean)
    latin_name = sqlalchemy.Column(sqlalchemy.String)
    variety = sqlalchemy.Column(sqlalchemy.String)
    type = sqlalchemy.Column(sqlalchemy.String)
    seed_spacing_inches = sqlalchemy.Column(sqlalchemy.Integer)
    row_spacing_inches = sqlalchemy.Column(sqlalchemy.Integer)
    seed_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    row_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_maturity = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_transplantation = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_seed_maturity = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_direct_sow = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_seed_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    indoor_seed_starting_date = sqlalchemy.Column(sqlalchemy.Integer)
    transplanting_date = sqlalchemy.Column(sqlalchemy.Date)
    direct_sow_date = sqlalchemy.Column(sqlalchemy.Date)
    harvest_date = sqlalchemy.Column(sqlalchemy.Date)
    seed_harvest_date = sqlalchemy.Column(sqlalchemy.Date)
    frost_sensitivity_rating = sqlalchemy.Column(sqlalchemy.Integer)

    
_engine = sqlalchemy.create_engine(_DATABASE_URL)

#-----------------------------------------------------------------------

def get_crop_info(crop_name):
    crop_infos = []

    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.type.ilike(crop_name + '%'),
            Crop_Info.template == True  # Filter for template being True
        )
        table = query.all()
        for row in table:
            crop_info = {'crop_id':row.crop_id, 'latin_name':row.latin_name, 'variety':row.variety, 'template':row.template,
                         'type':row.type, 'seed_spacing_inches':row.seed_spacing_inches, 'row_spacing_inches':row.row_spacing_inches,
                         'seed_spacing_harvest':row.seed_spacing_harvest, 'row_spacing_harvest':row.row_spacing_harvest,
                         'days_to_transplantation':row.days_to_transplantation, 'days_to_seed_maturity':row.days_to_seed_maturity,
                         'days_to_direct_sow':row.days_to_direct_sow, 'days_to_harvest':row.days_to_harvest,
                         'days_to_seed_harvest':row.days_to_seed_harvest, 'indoor_seed_starting_date':row.indoor_seed_starting_date,
                         'transplanting_date':row.transplanting_date, 'direct_sow_date':row.direct_sow_date, 'harvest_date':row.harvest_date,
                         'seed_harvest_date':row.seed_harvest_date, 'frost_sensitivity_rating':row.frost_sensitivity_rating}
            crop_infos.append(crop_info)

    return crop_infos
 
def add_crop(crop_info):
    with sqlalchemy.orm.Session(_engine) as session:
        new_crop = Crop_Info(**crop_info)
        session.add(new_crop)
        session.commit()



#-----------------------------------------------------------------------

def _test():
    crop_infos = get_crop_info('carrot')
    for crop_info in crop_infos:
        print(crop_info)
        print()

if __name__ == '__main__':
    _test()
