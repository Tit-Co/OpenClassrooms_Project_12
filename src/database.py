import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

def get_engine(database_url=None):
    return create_engine(
    database_url or DATABASE_URL,
    echo=False
)

def get_session(engine):
    return sessionmaker(bind=engine)
