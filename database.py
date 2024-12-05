from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")

try:
    engine = create_engine(DATABASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
except SQLAlchemyError as e:
    print(f"Error connecting to the database: {e}")

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    try:
        import your_models_here
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error initializing the database: {e}")

def get_db_session():
    try:
        return db_session
    except SQLAlchemyError as e:
        print(f"Error getting DB session: {e}")
        return None

class ExampleModel(Base):
    __tablename__ = 'example_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

def create_example_model(name):
    try:
        example = ExampleModel(name=name)
        db_session.add(example)
        db_session.commit()
    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error creating ExampleModel: {e}")

def main():
    init_db()
    create_example_model('Test Name')

if __name__ == '__main__':
    main()