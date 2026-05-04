from src.controllers.main_controller import MainController
from src.database import get_session, get_engine, DATABASE_URL


def main():
    db_engine = get_engine(database_url=DATABASE_URL)
    session_local = get_session(engine=db_engine)
    session = session_local()
    controller = MainController()
    controller.init_db(db_engine=db_engine, session=session)
    controller.run(session)


if __name__ == '__main__':
    main()
