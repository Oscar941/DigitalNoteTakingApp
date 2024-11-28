from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///database.db")  

engine = create_engine(DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import your_models_here  

    Base.metadata.create_all(bind=engine)

def get_db_session():
    return db_session

class ExampleModel(Base):
    __tablename__ = 'example_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))