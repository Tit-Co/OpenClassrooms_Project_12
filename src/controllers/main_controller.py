from src.seed import roles
from src.database import engine, SessionLocal
from src.models.base import Base
from src.models.role import Role
from src.models.user import Administrator
from src.views.main_view import MainView
from .collaborator_controller import CollaboratorController


class MainController:
    def __init__(self):
        self.view = MainView()
        self.user_controller = CollaboratorController(self)
        self.role_permissions = {
            "ADMINISTRATOR": ["display", "create:collaborator", "create:contract"],
            "COMMERCIAL": ["display", "create:client", "create:event"],
            "TECHNICIAN": ["display", "update:event"]
        }
        self.init_db()

    def init_db(self):
        Base.metadata.create_all(bind=engine)

        session = SessionLocal()
        for role in roles:
            if not session.query(Role).filter_by(name=role).first():
                session.add(Role(name=role))

        super_user = self.user_controller.init_super_user()
        role_id = session.query(Role).filter_by(name=super_user["role"]).first().id
        if not session.query(Administrator).filter_by(name=super_user["name"],
                                                     email=super_user["email"]).first():
            session.add(Administrator(
                name=super_user["name"],
                email=super_user["email"],
                password=super_user["password"],
                role_id=role_id
            ))

        session.commit()
        session.close()

    def run(self):
        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_main_menu()

            actions = {
                1: self.user_controller.login,
                2: self.goodbye
            }

            action = actions.get(menu)
            action()

    def goodbye(self):
        self.view.display_goodbye()
        exit(1)
