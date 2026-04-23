from src.controllers.main_controller import MainController
from src.database import SessionLocal


def main():
    session = SessionLocal()
    controller = MainController()
    controller.run(session)


if __name__ == '__main__':
    main()
