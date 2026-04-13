from src.database import engine
from src.models.base import Base

from src.models import client, contract, event


def init_db():
    Base.metadata.create_all(bind=engine)


def main():
    init_db()


if __name__ == '__main__':
    main()
