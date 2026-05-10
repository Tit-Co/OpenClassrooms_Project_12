from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import DATABASE, HOST, PASSWORD, PORT, USERNAME

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


def get_engine(database_url=None):
    return create_engine(database_url or DATABASE_URL, echo=False)


def get_session(engine):
    return sessionmaker(bind=engine)
