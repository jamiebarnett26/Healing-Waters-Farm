#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import IntegrityError
import dotenv

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()

class Family (Base):
    __tablename__ = 'family'
    family_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    family_name = sqlalchemy.Column(sqlalchemy.String)

class Species (Base):
    __tablename__ = 'species'
    species_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    family_id = sqlalchemy.Column(sqlalchemy.Integer)
    latin_name = sqlalchemy.Column(sqlalchemy.String)
    species_name = sqlalchemy.Column(sqlalchemy.String)

class Variety (Base):
    __tablename__ = 'variety'
    variety_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    species_id = sqlalchemy.Column(sqlalchemy.Integer)
    variety_name = sqlalchemy.Column(sqlalchemy.String)

class Crop_Info (Base):
    __tablename__ = 'crop_infos'
    crop_info_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    variety_id = sqlalchemy.Column(sqlalchemy.Integer)
    crop_type = sqlalchemy.Column(sqlalchemy.String)
    template = sqlalchemy.Column(sqlalchemy.Boolean)
    days_to_maturity = sqlalchemy.Column(sqlalchemy.Integer)
    plant_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    plant_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer)
    row_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    row_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_maturity_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_maturity_seed = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_transplantation = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_direct_sow = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    days_to_seed_harvest = sqlalchemy.Column(sqlalchemy.Integer)
    frost_sensitivity_rating = sqlalchemy.Column(sqlalchemy.Integer)

class User_Crop (Base):
    __tablename__ = 'user_crops'
    user_crop_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    crop_info_id = sqlalchemy.Column(sqlalchemy.Integer)
    indoor_seed_starting_date = sqlalchemy.Column(sqlalchemy.Date)
    transplanting_date = sqlalchemy.Column(sqlalchemy.Date)
    direct_sow_date = sqlalchemy.Column(sqlalchemy.Date)
    harvest_date = sqlalchemy.Column(sqlalchemy.Date)
    seed_harvest_date = sqlalchemy.Column(sqlalchemy.Date)

class Users (Base):
    __tablename__ = 'users'
    user_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    first_name = sqlalchemy.Column(sqlalchemy.String)
    last_name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)

class Admin (Base):
    __tablename__ = 'admin'
    admin_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)

_engine = sqlalchemy.create_engine(_DATABASE_URL)

class Tasks (Base):
    __tablename__ = 'tasks'
    task_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_crop_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    task_name = sqlalchemy.Column(sqlalchemy.String(255))
    task_date = sqlalchemy.Column(sqlalchemy.Date)



def add_user(first_name, last_name, email):
    with sqlalchemy.orm.Session(_engine) as session:
        is_existing_user = session.query(Users).filter_by(email=email).first()
        if is_existing_user:
            print("User already exists with email:", email)
            return is_existing_user
        
        new_user = Users(first_name=first_name, last_name=last_name, email=email)
        try:
            session.add(new_user)
            session.commit()  # Commit the transaction
            print("New user committed:", email)
        except IntegrityError as e:
            session.rollback()
            print("IntegrityError encountered:", e)
            return None
        
        # Fetch the newly added user in the same session
        user = session.query(Users).filter_by(email=email).first()
        return user



def get_user(searchvalue, searchfield):
    with sqlalchemy.orm.Session(_engine) as session:
        if searchfield == 'email':
            query = session.query(Users).filter_by(email=searchvalue)
            
        else:
            query = session.query(Users).filter_by(user_id=searchvalue)

        table = query.first()
        return table


def is_admin(user_id):
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Admin).filter_by(user_id=user_id)
        table = query.first()

        if table:
            return 'true'
        return 'false'
def get_profiles():
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Users)
        table = query.all()
        profiles = []
        for row in table:
            profile = {
                'first_name':row.first_name,
                'last_name':row.last_name,
                'email':row.email
            }
            profiles.append(profile)

        return profiles

#------------------------------------------------------------------------------
# search_value: This is the value that the user either clicks on or types in.
#               It represents the term that we want to search for in the database.
# search_field: This is the key used to look up the corresponding database column
#               in the 'search_fields_map' dictionary. 
#------------------------------------------------------------------------------

def search_field_name(search_field, search_value):
    results = []
    with sqlalchemy.orm.Session(_engine) as session:
        if search_field == 'family':
            query = session.query(Family).filter(
                Family.family_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                family = {
                    'family_id':row.family_id,
                    'family_name':row.family_name
            }
                results.append(family)

        if search_field == 'species':
            query = session.query(Species).filter(
                Species.species_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                species = {
                    'species_id':row.species_id,
                    'family_id':row.family_id,
                    'latin_name':row.latin_name,
                    'species_name':row.species_name
            }
                results.append(species)
  
        
        if search_field == 'variety':
            query = session.query(Variety).filter(
                Variety.variety_name.ilike(f"%{search_value}%"),
            )
            table = query.all()
            for row in table:
                variety = {
                    'variety_id':row.variety_id,
                    'species_id':row.species_id,
                    'variety_name':row.variety_name
            }
                results.append(variety)
    return results

def search_field_id(search_field, search_value):
    results = []
    with sqlalchemy.orm.Session(_engine) as session:
        if search_field == 'family':
            query = session.query(Family).filter(
                Family.family_id == search_value
            )
            table = query.all()
            for row in table:
                family = {
                    'family_id':row.family_id,
                    'family_name':row.family_name
            }
                results.append(family)

        if search_field == 'species':
            query = session.query(Species).filter(
                Species.species_id == search_value,
            )
            table = query.all()
            for row in table:
                species = {
                    'species_id':row.species_id,
                    'family_id':row.family_id,
                    'latin_name':row.latin_name,
                    'species_name':row.species_name
            }
                results.append(species)
  
        
        if search_field == 'variety':
            query = session.query(Variety).filter(
                Variety.variety_id == search_value,
            )
            table = query.all()
            for row in table:
                variety = {
                    'variety_id':row.variety_id,
                    'species_id':row.species_id,
                    'variety_name':row.variety_name
            }
                results.append(variety)
    return results

def species_from_family(family_id):
    species = []
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Species).filter(
            Species.family_id == family_id
        )
        table = query.all()
        for row in table:
            spec = {
                'species_id': row.species_id,
                'family_id': family_id,
                'latin_name': row.latin_name,
                'species_name': row.species_name
            }
            species.append(spec)
    return species

def variety_from_species(species_id):
    varieties = []
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Variety).filter(
            Variety.species_id == species_id
        )
        table = query.all()
        for row in table:
            variety = {
                'variety_id': row.variety_id,
                'species_id': species_id,
                'variety_name': row.variety_name
            }
            varieties.append(variety)
    return varieties

def crop_info_from_variety(variety_id):
    crop_infos = []
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.variety_id == variety_id
        )
        
        table = query.all()
        for row in table:
            crop_info = {
                'crop_info_id': row.crop_info_id,  # Use ':' instead of '='
                'variety_id': variety_id,
                'crop_type': row.crop_type,
                'template': row.template,
                'days_to_maturity': row.days_to_maturity,
                'plant_spacing_harvest': row.plant_spacing_harvest,
                'plant_spacing_seed': row.plant_spacing_seed,
                'row_spacing_harvest': row.row_spacing_harvest,
                'row_spacing_seed': row.row_spacing_seed, 
                'days_to_maturity_harvest': row.days_to_maturity_harvest,
                'days_to_maturity_seed': row.days_to_maturity_seed,
                'days_to_transplantation': row.days_to_transplantation,
                'days_to_direct_sow': row.days_to_direct_sow,
                'days_to_harvest': row.days_to_harvest,
                'days_to_seed_harvest': row.days_to_seed_harvest,
                'frost_sensitivity_rating': row.frost_sensitivity_rating
            }

            crop_infos.append(crop_info)
    return crop_infos

def family_from_species(species_id):
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Species).filter(
            Species.species_id == species_id
        )
        species_table = query.first()
        query = session.query(Family).filter(
            Family.family_id == species_table.family_id
        )
        family_table = query.first()
        return family_table

def species_from_variety(variety_id):
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Variety).filter(
            Variety.variety_id == variety_id
        )
        variety_table = query.first()
        query = session.query(Species).filter(
            Species.species_id == variety_table.species_id
        )
        species_table = query.first()
        return species_table


def full_crop_info(crop_info_id):
    with sqlalchemy.orm.Session(_engine) as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.crop_info_id == crop_info_id
        )
        info_table = query.first()
        if not info_table:
            return None  # Ensure you handle None to avoid AttributeError

        query = session.query(Variety).filter(
            Variety.variety_id == info_table.variety_id
        )
        variety_table = query.first()
        if not variety_table:
            return None  # Similarly, handle None for variety_table

        species_table = species_from_variety(info_table.variety_id)
        if not species_table:
            return None  # Check for None before proceeding to avoid crashes

        family_table = family_from_species(species_table.family_id)
        if not family_table:
            return None

        crop_info = {
            'variety_id': variety_table.variety_id,  # Include variety_id explicitly
            'family_name': family_table.family_name,
            'latin_name': species_table.latin_name,
            'variety_name': variety_table.variety_name,
            'crop_type': info_table.crop_type,
            'template': info_table.template,
            'days_to_maturity': info_table.days_to_maturity,
            'plant_spacing_harvest': info_table.plant_spacing_harvest,
            'plant_spacing_seed': info_table.plant_spacing_seed,
            'row_spacing_harvest': info_table.row_spacing_harvest,
            'row_spacing_seed': info_table.row_spacing_seed,
            'days_to_maturity_harvest': info_table.days_to_maturity_harvest,
            'days_to_maturity_seed': info_table.days_to_maturity_seed,
            'days_to_transplantation': info_table.days_to_transplantation,
            'days_to_direct_sow': info_table.days_to_direct_sow,
            'days_to_harvest': info_table.days_to_harvest,
            'days_to_seed_harvest': info_table.days_to_seed_harvest,
            'frost_sensitivity_rating': info_table.frost_sensitivity_rating
        }
        return crop_info


def get_template_crop(species_id):
    with sqlalchemy.orm.Session(_engine) as session:
        varieties = variety_from_species(species_id)
        variety_ids = []
        for variety in varieties:
            variety_ids.append(variety['variety_id'])
        # Now, retrieve all Crop_Info entries for the found variety IDs
        crop_info_id = session.query(Crop_Info.crop_info_id).filter(
            Crop_Info.variety_id.in_(variety_ids),
            Crop_Info.template == True
        ).first()
    if crop_info_id is not None:
        return crop_info_id[0]
    else:
        return -1

def get_user_crops(user_id):
     with sqlalchemy.orm.Session(_engine) as session:
        table = session.query(User_Crop).filter(
            User_Crop.user_id == user_id
        ).all()

        user_crops = []
        for row in table:
            user_crop = {
                'user_crop_id':row.user_crop_id,
                'user_id':row.user_id,
                'crop_info_id':row.crop_info_id,
                'indoor_seed_starting_date':row.indoor_seed_starting_date,
                'transplanting_date':row.transplanting_date,
                'direct_sow_date':row.direct_sow_date,
                'harvest_date':row.harvest_date,
                'seed_harvest_date':row.seed_harvest_date
            }
            user_crops.append(user_crop)
        return user_crops

def edit_user_tasks(user_id, user_crop_id, date_field, new_date):
    with sqlalchemy.orm.Session(_engine) as session:

        user_crops = session.query(User_Crop).filter(User_Crop.user_id == user_id).all()
        for crop in user_crops:
            if hasattr(crop, date_field):  
                setattr(crop, date_field, new_date) 
        session.commit()

        
def add_task(user_id, user_crop_id, task_name, task_date):
    with sqlalchemy.orm.Session(_engine) as session:
        new_task = Tasks(
            user_crop_id=user_crop_id, 
            user_id=user_id, 
            task_name=task_name, 
            task_date=task_date)
        session.add(new_task)
        session.commit()

def get_user_added_tasks(user_crop_id, todos):
    with sqlalchemy.orm.Session(_engine) as session:
        user_tasks = session.query(Tasks).filter(
            Tasks.user_crop_id == user_crop_id
        ).all()

        for task in user_tasks:
            todos.append({
                "user_crop_id": task.user_crop_id,
                "task": task.task_name,
                "date": task.task_date,
                "done": False
            })
        
        return todos

def add_family(family):
    with sqlalchemy.orm.Session(_engine) as session:
        new_family = Family(**family)
        session.add(new_family)
        session.commit()

def add_species(species):
    with sqlalchemy.orm.Session(_engine) as session:
        new_species = Species(**species)
        session.add(new_species)
        session.commit()

def add_variety(variety, crop_info):
    crop_info = {key: (None if value == 'None' else value) for key, value in crop_info.items()}
    with sqlalchemy.orm.Session(_engine) as session:
        new_variety = Variety(**variety)
        session.add(new_variety)
        session.commit()

        crop_info['variety_id'] = new_variety.variety_id

        new_crop_info = Crop_Info(**crop_info)
        session.add(new_crop_info)
        session.commit()

def add_user_crop(user_crop):
    with sqlalchemy.orm.Session(_engine) as session:
        new_crop = User_Crop(**user_crop)
        session.add(new_crop)
        session.commit()

def delete_family(family_id):
    with sqlalchemy.orm.Session(_engine) as session:
        family_to_delete = session.query(Family).filter_by(family_id=family_id).first()

        species = species_from_family(family_id)
        for spec in species:
            delete_species(spec['species_id'])

        session.delete(family_to_delete)
        session.commit()

def delete_species(species_id):
    with sqlalchemy.orm.Session(_engine) as session:
        species_to_delete = session.query(Species).filter_by(species_id=species_id).first()

        varieties = variety_from_species(species_id)
        for variety in varieties:
            delete_variety(variety['variety_id'])

        session.delete(species_to_delete)
        session.commit()
    
def delete_variety(variety_id):
    with sqlalchemy.orm.Session(_engine) as session:
        variety_to_delete = session.query(Variety).filter_by(variety_id=variety_id).first()

        crop_infos = crop_info_from_variety(variety_id)
        for crop_info in crop_infos:
            crop_info_to_delete = session.query(Crop_Info).filter_by(crop_info_id=crop_info['crop_info_id']).first()
            session.delete(crop_info_to_delete)
            session.commit()

        session.delete(variety_to_delete)
        session.commit()


#-----------------------------------------------------------------------

def _test():


    print(is_admin(1))
    print(is_admin(3))

    # results = search_field('family', '')
    # print(results)
    # results = search_field('species', '')
    # print(results)

    # species = species_from_family(1)
    # print(species)

    # varieties = variety_from_species(1)
    # print(varieties)

    # crop_infos = crop_info_from_variety(1)
    # print(crop_infos)

if __name__ == '__main__':
    _test()