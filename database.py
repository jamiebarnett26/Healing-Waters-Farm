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

def edit_task_date(task_id, new_date):
    with sqlalchemy.orm.Session(_engine) as session:
        task = session.query(Tasks).filter(Tasks.task_id == task_id).first()
        if task:
            task.task_date = new_date
            session.commit()
        else:
            raise ValueError("Task not found")
        
def delete_task(task_id):
    with sqlalchemy.orm.Session(_engine) as session:
        task = session.query(Tasks).filter(Tasks.task_id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
        else:
            raise ValueError("Task not found")

def delete_template(user_crop_id):
    with sqlalchemy.orm.Session(_engine) as session:
        user_tasks =  session.query(Tasks).filter(Tasks.user_crop_id == user_crop_id).all()
        for user_task in user_tasks:
            delete_task(user_task.task_id)
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