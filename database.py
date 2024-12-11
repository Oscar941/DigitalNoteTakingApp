from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")

try:
    database_engine = create_engine(DB_URI, convert_unicode=True)
    database_session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=database_engine))
except SQLAlchemyError as error:
    print(f"Error connecting to the database: {error}")

BaseModel = declarative_base()
BaseModel.query = database_session.query_property()

def initialize_database():
    try:
        import models
        BaseModel.metadata.create_all(bind=database_engine)
    except Exception as error:
        print(f"Error initializing the database: {error}")

def get_database_session():
    try:
        return database_session
    except SQLAlchemyError as error:
        print(f"Error getting DB session: {error}")
        return None

class NoteModel(BaseModel):
    __tablename__ = 'note_model'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))

def add_note_model(title):
    try:
        note = NoteModel(title=title)
        database_session.add(note)
        database_session.commit()
    except SQLAlchemyError as error:
        database_session.rollback()
        print(f"Error adding NoteModel: {error}")

def run_demo():
    initialize_database()
    add_note_model('Demo Note Title')

if __name__ == '__main__':
    run_demo()