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

    def init_super_user(self):
        return {
            "name": admin_credentials["name"],
            "email": admin_credentials["email"],
            "password": self.hash_password(admin_credentials["password"]),
            "role": admin_credentials["role"]
        }

    def init_db(self, db_engine, session):
        Base.metadata.create_all(bind=db_engine)

        for role in roles:
            if not session.query(Role).filter_by(name=role).first():
                session.add(Role(name=role))

        super_user = self.init_super_user()

        role = session.query(Role).filter_by(name=super_user["role"]).first()

        if role and not session.query(Administrator).filter_by(
                name=super_user["name"],
                email=super_user["email"]
        ).first():
            session.add(Administrator(
                name=super_user["name"],
                email=super_user["email"],
                password=super_user["password"],
                role_id=role.id
            ))

        session.commit()

    def run(self, session):
        self.init_db(engine, session)

        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_menu(2)

            actions = {
                1: lambda : self.login(session=session),
                2: self.goodbye
            }

            action = actions.get(menu)
            action()

    def login(self, session):
        while True:
            self.view.display_login_submenu()
            menu = self.view.prompt_for_continuing()

            if menu == 'q':
                break

            email = self.view.prompt_for_email()

            password = self.view.prompt_for_password()

            success = self.authenticate(session, email, password)

            if success:
                self.user_controller.collaborator_menu(session=session)
                break

    def authenticate(self, session, email, password):
        models = [Commercial, Technician, Administrator]
        user = None

        for model in models:
            user = session.query(model).filter_by(email=email).first()
            if user:
                break

        if user is None:
            self.view.display_collaborator_does_not_exist()
            return False

        if not self.check_password(password, user.password):
            self.view.display_wrong_password()
            return False

        self.init_permissions(user)
        return True

    @staticmethod
    def check_password(password, user_password):
        if isinstance(user_password, str):
            user_password = user_password.encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), user_password)

    @staticmethod
    def hash_password(password):
        return  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def init_permissions(self, user):
        self.user_controller.permissions = self.role_permissions.get(user.role.name)
        self.view.display_successfully_logged_in(user.name)

    def goodbye(self):
        self.view.display_goodbye()
        exit(1)
