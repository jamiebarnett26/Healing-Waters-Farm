#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------

import os
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy.exc import IntegrityError
import sys
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
    days_to_maturity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    plant_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    plant_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    row_spacing_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    row_spacing_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_maturity_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_maturity_seed = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_transplantation = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_direct_sow = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    days_to_seed_harvest = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
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

class Question (Base):
    __tablename__ = 'questions'
    question_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_name = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now(), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)

class Reply (Base):
    __tablename__ = 'replies'
    reply_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_name = sqlalchemy.Column(sqlalchemy.String)
    question_id = sqlalchemy.Column(sqlalchemy.Integer)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now(), nullable=False)
    text = sqlalchemy.Column(sqlalchemy.String)

class Announcement (Base):
    __tablename__ = 'announcements'
    announcement_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_name = sqlalchemy.Column(sqlalchemy.String)
    created_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), nullable=False)
    updated_at = sqlalchemy.Column(sqlalchemy.TIMESTAMP, server_default=sqlalchemy.func.now(), onupdate=sqlalchemy.func.now(), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)

class Tasks (Base):
    __tablename__ = 'tasks'
    task_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_crop_id = sqlalchemy.Column(sqlalchemy.Integer)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    task_name = sqlalchemy.Column(sqlalchemy.String(255))
    task_date = sqlalchemy.Column(sqlalchemy.Date)
    completed = sqlalchemy.Column(sqlalchemy.Boolean)


_engine = sqlalchemy.create_engine(_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=_engine))

def get_session():
    """Helper function to retrieve a session from the scoped session factory"""
    return Session()

def checkbox(task_id, completed):
    with get_session() as session:
        print(completed, file=sys.stderr)
        query = session.query(Tasks).filter_by(task_id=task_id)
        task = query.first()
        if task: 
            task.completed = completed
            session.commit()

def add_question(question):
    with get_session() as session:
        new_question = Question(**question)
        session.add(new_question)
        session.commit()
    return

def add_reply(reply):
    with get_session() as session:
        new_reply = Reply(**reply)
        session.add(new_reply)
        session.commit()
    return

def add_announcement(announcement):
    with get_session() as session:
        new_announcement = Announcement(**announcement)
        session.add(new_announcement)
        session.commit()
    return



def add_user(first_name, last_name, email):
    with get_session() as session:
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
    with get_session() as session:
        if searchfield == 'email':
            query = session.query(Users).filter_by(email=searchvalue)
            
        else:
            query = session.query(Users).filter_by(user_id=searchvalue)

        table = query.first()
        return table


def is_admin(user_id):
    with get_session() as session:
        query = session.query(Admin).filter_by(user_id=user_id)
        table = query.first()

        if table:
            return 'true'
        return 'false'
def get_profiles():
    with get_session() as session:
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

def get_questions():
    with get_session() as session:
        query = session.query(Question)
        table = query.all()
        questions = []
        for row in table:
           question = {
                'question_id':row.question_id,
                'user_id':row.user_id,
                'user_name':row.user_name,
                'created_at':row.created_at,
                'title':row.title,
                'text':row.text,
                'status':row.status
            }
           questions.append(question)

        return questions

def get_replies():
    with get_session() as session:
        query = session.query(Reply)
        table = query.all()
        replies = []
        for row in table:
           reply = {
                'reply_id':row.reply_id,
                'question_id':row.question_id,
                'user_id':row.user_id,
                'user_name':row.user_name,
                'created_at':row.created_at,
                'text':row.text,
            }
           replies.append(reply)

        return replies

def get_announcements():
    with get_session() as session:
        query = session.query(Announcement)
        table = query.all()
        announcements = []
        for row in table:
           announcement = {
                'announcement_id':row.announcement_id,
                'user_id':row.user_id,
                'user_name':row.user_name,
                'created_at':row.created_at,
                'text':row.text,
                'title':row.title,
            }
           announcements.append(announcement)

        return announcements

#------------------------------------------------------------------------------
# search_value: This is the value that the user either clicks on or types in.
#               It represents the term that we want to search for in the database.
# search_field: This is the key used to look up the corresponding database column
#               in the 'search_fields_map' dictionary. 
#------------------------------------------------------------------------------

def search_field_name(search_field, search_value):
    results = []
    with get_session() as session:
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
    with get_session() as session:
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
        
        if search_field == 'crop_info':
            query = session.query(Crop_Info).filter(
                Crop_Info.crop_info_id == search_value,
            )
            table = query.all()
            for row in table:
                crop_info = {
                'crop_info_id': row.crop_info_id,  # Use ':' instead of '='
                'variety_id': row.variety_id,
                'crop_type': row.crop_type,
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
                results.append(crop_info)
        if search_field == 'question':
            query = session.query(Question).filter(
                Question.question_id == search_value,
            )
            table = query.all()
            for row in table:
                question = {
                    'question_id':row.question_id,
                    'user_id':row.user_id,
                    'user_name':row.user_name,
                    'created_at':row.created_at,
                    'updated_at':row.updated_at,
                    'title':row.title,
                    'text':row.text,
                    'status':row.status
                }
                results.append(question)
        if search_field == 'reply':
            query = session.query(Reply).filter(
                Reply.reply_id == search_value,
            )
            table = query.all()
            for row in table:
                reply = {
                    'reply_id':row.reply_id,
                    'question_id':row.question_id,
                    'user_id':row.user_id,
                    'user_name':row.user_name,
                    'created_at':row.created_at,
                    'updated_at':row.updated_at,
                    'text':row.text,
                }
                results.append(reply)
        if search_field == 'announcement':
            query = session.query(Announcement).filter(
                Announcement.announcement_id == search_value,
            )
            table = query.all()
            for row in table:
                announcement = {
                    'announcement_id':row.announcement_id,
                    'user_id':row.user_id,
                    'user_name':row.user_name,
                    'created_at':row.created_at,
                    'updated_at':row.updated_at,
                    'title':row.title,
                    'text':row.text,
                }
                results.append(announcement)
    return results

def species_from_family(family_id):
    species = []
    with get_session() as session:
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
    with get_session() as session:
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
    with get_session() as session:
        query = session.query(Crop_Info).filter(
            Crop_Info.variety_id == variety_id
        )
        
        table = query.all()
        for row in table:
            crop_info = {
                'crop_info_id': row.crop_info_id,  # Use ':' instead of '='
                'variety_id': variety_id,
                'crop_type': row.crop_type,
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
    with get_session() as session:
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
    with get_session() as session:
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
    with get_session() as session:
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

        family_table = family_from_species(species_table.species_id)
        if not family_table:
            return None

        crop_info = {
            'variety_id': variety_table.variety_id,  # Include variety_id explicitly
            'family_name': family_table.family_name,
            'latin_name': species_table.latin_name,
            'variety_name': variety_table.variety_name,
            'crop_type': info_table.crop_type,
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

def get_user_crops(user_id):
     with get_session() as session:
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

def edit_tasks(task_id, task_name, new_date):
    with sqlalchemy.orm.Session(_engine) as session:
        task = session.query(Tasks).filter(Tasks.task_id == task_id).first()
        task.task_name = task_name
        task.task_date = new_date
        session.commit()

def delete_template(user_crop_id):
    with sqlalchemy.orm.Session(_engine) as session:
        session.query(User_Crop).filter(User_Crop.user_crop_id == user_crop_id).delete()
        session.commit()


        
def add_task(user_id, user_crop_id, task_name, task_date):
    with sqlalchemy.orm.Session(_engine) as session:
        new_task = Tasks(
            user_crop_id=user_crop_id, 
            user_id=user_id, 
            task_name=task_name, 
            task_date=task_date,
            completed=False)
        session.add(new_task)
        session.commit()

def get_tasks(user_crop_id):
    with sqlalchemy.orm.Session(_engine) as session:
        user_tasks = session.query(Tasks).filter(
            Tasks.user_crop_id == user_crop_id
        ).all()

        todos = []

        for task in user_tasks:
            todos.append({
                "user_crop_id": task.user_crop_id,
                "task_id":task.task_id,
                "task": task.task_name,
                "date": task.task_date,
                "completed": task.completed
            })
        
        return todos

def add_family(family):
    with get_session() as session:
        new_family = Family(**family)
        session.add(new_family)
        session.commit()

def add_species(species):
     with get_session() as session:
        new_species = Species(**species)
        session.add(new_species)
        session.commit()

def add_variety(variety, crop_info):
    crop_info = {key: (None if value == 'None' else value) for key, value in crop_info.items()}
    with get_session() as session:
        new_variety = Variety(**variety)
        session.add(new_variety)
        session.commit()

        crop_info['variety_id'] = new_variety.variety_id

        new_crop_info = Crop_Info(**crop_info)
        session.add(new_crop_info)
        session.commit()

def edit_family(family_id, updated_data):
    with get_session() as session:
        family = session.query(Family).get(family_id)
        if family:
            for key, value in updated_data.items():
                setattr(family, key, value)
            session.commit()

def edit_species(species_id, updated_data):
    with get_session() as session:
        species = session.query(Species).get(species_id)
        if species:
            for key, value in updated_data.items():
                setattr(species, key, value)
            session.commit()

def edit_variety(variety_id, updated_data_variety, updated_data_crop):
    for field in updated_data_crop:
        if updated_data_crop.get(field) == "":
            updated_data_crop[field] = None 

    with get_session() as session:
        crop_info = session.query(Crop_Info).get(variety_id)
        variety = session.query(Variety).get(variety_id)
        if crop_info:
            for key, value in updated_data_crop.items():
                setattr(crop_info, key, value)
                session.commit()
        if variety:
            for key, value in updated_data_variety.items():
                setattr(variety, key, value)
                session.commit()

def edit_question(question_id, updated_data):
    with get_session() as session:
        question = session.query(Question).get(question_id)
        if question:
            for key, value in updated_data.items():
                setattr(question, key, value)
            session.commit()

def edit_reply(reply_id, updated_data):
    with get_session() as session:
        reply = session.query(Reply).get(reply_id)
        if reply:
            for key, value in updated_data.items():
                setattr(reply, key, value)
            session.commit()

def edit_announcement(announcement_id, updated_data):
    with get_session() as session:
        announcement = session.query(Announcement).get(announcement_id)
        if announcement:
            for key, value in updated_data.items():
                setattr(announcement, key, value)
            session.commit()

def add_user_crop(user_crop, user_id):
    with get_session() as session:
        # Add the new user crop
        new_crop = User_Crop(**user_crop)
        session.add(new_crop)
        session.commit()  # Commit to get the generated user_crop_id
        
        # Get the generated primary key
        user_crop_id = new_crop.user_crop_id  # Access the primary key after commit
        
        # Add tasks if relevant dates exist
        if user_crop.get("indoor_seed_starting_date"):
            add_task(user_id, user_crop_id, "Start indoor seeding", user_crop["indoor_seed_starting_date"])
        if user_crop.get("transplanting_date"):
            add_task(user_id, user_crop_id, "Transplant plants outdoors", user_crop["transplanting_date"])
        if user_crop.get("direct_sow_date"):
            add_task(user_id, user_crop_id, "Direct sowing", user_crop["direct_sow_date"])
        if user_crop.get("harvest_date"):
            add_task(user_id, user_crop_id, "Prepare for harvest", user_crop["harvest_date"])
        if user_crop.get("seed_harvest_date"):
            add_task(user_id, user_crop_id, "Prepare for seed harvest", user_crop["seed_harvest_date"])


def delete_family(family_id):
    with get_session() as session:
        family_to_delete = session.query(Family).filter_by(family_id=family_id).first()

        species = species_from_family(family_id)
        for spec in species:
            delete_species(spec['species_id'])

        session.delete(family_to_delete)
        session.commit()

def delete_species(species_id):
    with get_session() as session:
        species_to_delete = session.query(Species).filter_by(species_id=species_id).first()

        varieties = variety_from_species(species_id)
        for variety in varieties:
            delete_variety(variety['variety_id'])

        session.delete(species_to_delete)
        session.commit()
    
def delete_variety(variety_id):
    with get_session() as session:
        variety_to_delete = session.query(Variety).filter_by(variety_id=variety_id).first()

        crop_infos = crop_info_from_variety(variety_id)
        for crop_info in crop_infos:
            crop_info_to_delete = session.query(Crop_Info).filter_by(crop_info_id=crop_info['crop_info_id']).first()
            session.delete(crop_info_to_delete)
            session.commit()

        session.delete(variety_to_delete)
        session.commit()

def delete_question(user_id, question_id):
    with get_session() as session:
        question_to_delete = session.query(Question).filter_by(question_id=question_id).first()
        if(str(user_id) == str(question_to_delete.user_id)):
            session.delete(question_to_delete)
            session.commit()

def delete_reply(user_id, reply_id):
    with get_session() as session:
        reply_to_delete = session.query(Reply).filter_by(reply_id=reply_id).first()
        if(str(user_id) == str(reply_to_delete.user_id)):
            session.delete(reply_to_delete)
            session.commit()


def delete_announcement(user_id, announcement_id):
    with get_session() as session:
        announcement_to_delete = session.query(Announcement).filter_by(announcement_id=announcement_id).first()
        if(str(user_id) == str(announcement_to_delete.user_id)):
            session.delete(announcement_to_delete)
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