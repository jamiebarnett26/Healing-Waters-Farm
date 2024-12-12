from database import sqlalchemy, os, dotenv

#-----------------------------------------------------------------------

dotenv.load_dotenv()
_DATABASE_URL = os.environ['DATABASE_URL']
_DATABASE_URL = _DATABASE_URL.replace('postgres://', 'postgresql://')

#-----------------------------------------------------------------------

Base = sqlalchemy.orm.declarative_base()
_engine = sqlalchemy.create_engine(_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30, pool_recycle=3600)
Session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=_engine))


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

#-----------------------------------------------------------------------

def get_session():
    """Helper function to retrieve a session from the scoped session factory"""
    return Session()

def search_field_id(search_field, search_value):
    results = []
    with get_session() as session:
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
