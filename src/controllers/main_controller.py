import bcrypt

from src.seed import roles
from src.database import engine, SessionLocal
from src.models.base import Base
from src.models.role import Role
from src.models.user import Administrator, Commercial, Technician
from src.views.main_view import MainView
from .collaborator_controller import CollaboratorController
from src.seed import admin_credentials


class MainController:
    def __init__(self):
        self.view = MainView()
        self.user_controller = CollaboratorController(self)
        self.role_permissions = {
            "ADMINISTRATOR": ["display:administrator", "display:commercial", "display:technician",
                              "create:administrator", "create:commercial", "create:technician",
                              "update:administrator", "update:commercial", "update:technician",
                              "delete:administrator", "delete:commercial", "delete:technician",
                              "display:contract", "display:client", "display:event",
                              "create:contract", "update:contract", "delete:contract",
                              "update:event", "filter:event"],

            "COMMERCIAL": ["display:administrator", "display:commercial", "display:technician",
                           "display:contract", "display:client", "display:event",
                           "create:client", "update:client", "delete:client", "update:contract",
                           "filter:contract", "create:event"],

            "TECHNICIAN": ["display:administrator", "display:commercial", "display:technician",
                           "display:contract", "display:client", "display:event", "update:event",
                           "filter:event"]
        }
        self.init_db()

    def init_super_user(self):
        return {
            "name": admin_credentials["name"],
            "email": admin_credentials["email"],
            "password": self.hash_password(admin_credentials["password"]),
            "role": admin_credentials["role"]
        }

    def init_db(self):
        Base.metadata.create_all(bind=engine)

        session = SessionLocal()
        for role in roles:
            if not session.query(Role).filter_by(name=role).first():
                session.add(Role(name=role))

        super_user = self.init_super_user()
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
            menu = self.view.prompt_for_menu(2)

            actions = {
                1: self.login,
                2: self.goodbye
            }

            action = actions.get(menu)
            action()

    def login(self):
        while True:
            self.view.display_login_submenu()
            menu = self.view.prompt_for_continuing()

            if menu == 'q':
                break

            email = self.view.prompt_for_email()

            models = [Commercial, Technician, Administrator]

            session = SessionLocal()
            user = None
            for model in models:
                user = session.query(model).filter_by(email=email).first()
                if user:
                    break

            if user is None:
                self.view.display_collaborator_does_not_exist()
                session.close()
                continue

            password = self.view.prompt_for_password()

            if not self.check_password(password, user):
                self.view.display_wrong_password()
                session.close()
                continue

            self.authenticate_user(user.name, user.email, user.password)

            session.close()

            self.user_controller.collaborator_menu()

    @staticmethod
    def check_password(password, user):
        return bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))

    @staticmethod
    def hash_password(password):
        return  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def authenticate_user(self, name, email, password):
        self.user_controller.init_user(email, password)
        self.view.display_successfully_logged_in(name)

    def goodbye(self):
        self.view.display_goodbye()
        exit(1)
