import bcrypt
from sqlalchemy import Engine
from sqlalchemy.orm import InstrumentedAttribute, Session

from src.database import engine
from src.models.base import Base
from src.models.role import Role
from src.models.user import Commercial, Manager, Technician
from src.seed import admin_credentials, roles
from src.views.main_view import MainView

from .client_controller import ClientController
from .collaborator_controller import CollaboratorController
from .contract_controller import ContractController
from .event_controller import EventController


class MainController:
    def __init__(self):
        self.view = MainView()

        self.user_controller = CollaboratorController(self)
        self.contract_controller = ContractController(self)
        self.client_controller = ClientController(self)
        self.event_controller = EventController(self)

        self.role_permissions = {
            "MANAGER": ["display:manager", "display:commercial", "display:technician",
                        "create:collaborator", "update:collaborator", "delete:collaborator",
                        "display:contract", "display:client", "display:event",
                        "create:contract", "update:contract", "delete:contract",
                        "update:event", "delete:event", "filter:event", "filter:client",
                        "filter:manager", "filter:commercial", "filter:technician"],

            "COMMERCIAL": ["display:manager", "display:commercial", "display:technician",
                           "display:contract", "display:client", "display:event",
                           "create:client", "update:client", "delete:client", "update:contract",
                           "filter:contract", "create:event", "filter:client",
                           "filter:manager", "filter:commercial", "filter:technician"],

            "TECHNICIAN": ["display:manager", "display:commercial", "display:technician",
                           "display:contract", "display:client", "display:event", "update:event",
                           "filter:event", "filter:client", "filter:collaborator",
                           "filter:manager", "filter:commercial", "filter:technician"]
        }

    def init_super_user(self) -> dict:
        """
        Method to initialize superuser as (the first) Manager
        Returns:
        A dictionary with superuser data
        """
        return {
            "name": admin_credentials["name"],
            "email": admin_credentials["email"],
            "password": self.hash_password(admin_credentials["password"]),
            "role": admin_credentials["role"]
        }

    def init_db(self, db_engine: Engine, session: Session) -> None:
        """
        Method to initialize database
        Args:
            db_engine (Engine): database engine
            session (Session): session
        """
        Base.metadata.create_all(bind=db_engine)

        for role in roles:
            if not session.query(Role).filter_by(name=role).first():
                session.add(Role(name=role))

        super_user = self.init_super_user()

        role = session.query(Role).filter_by(name=super_user["role"]).first()

        if role and not session.query(Manager).filter_by(
                name=super_user["name"],
                email=super_user["email"]
        ).first():
            session.add(Manager(
                name=super_user["name"],
                email=super_user["email"],
                password=super_user["password"],
                role_id=role.id
            ))

        session.commit()

    def run(self, session: Session) -> None:
        """
        Method to run the application
        Args:
            session (Session): session
        """
        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_menu(2)

            actions = {
                1: lambda : self.login(session=session),
                2: self.goodbye
            }

            action = actions.get(menu)
            action()

    def login(self, session: Session, email: str, password: str) -> bool:
        """
        Method to launch login
        Args:
            session (Session): session
            email (str): email
            password (str): password
        """
        self.init_db(engine, session)

        return self.authenticate(session=session, email=email, password=password)

    def authenticate(self, session: Session, email: str, password: str) -> bool | None:
        """
        Method to authenticate user and initialize user permissions
        Args:
            session (Session): session
            email (str): email
            password (str): password

        Returns:
        A boolean indicating success or failure in authentication
        """
        models = [Commercial, Technician, Manager]
        user = None

        for model in models:
            user = session.query(model).filter_by(email=email).first()
            if user:
                break

        if user is None:
            return None

        if not self.check_password(password=password, user_password=user.password):
            return False

        self.init_permissions(session=session, user=user)

        self.user_controller.save_current_user(email=email)

        return True

    @staticmethod
    def check_password(password: str, user_password: InstrumentedAttribute) -> bool:
        """
        Method to check if password matches hashed password
        Args:
            password (str): password
            user_password (bytes): hashed password

        Returns:
        A boolean indicating success or failure in checking password
        """
        if isinstance(user_password, str):
            user_password = user_password.encode("utf-8")

        return bcrypt.checkpw(password=password.encode("utf-8"), hashed_password=user_password)

    @staticmethod
    def hash_password(password: str | bytes) -> bytes:
        """
        Method to hash and salt password
        Args:
            password (str | bytes): password

        Returns:
        The hashed password
        """
        if isinstance(password, str):
            password = password.encode("utf-8")

        return  bcrypt.hashpw(password=password, salt=bcrypt.gensalt())

    def init_permissions(self, session: Session,
                         user: type[Commercial] | type[Manager] | type[Technician]) -> None:
        """
        Method to initialize permissions
        Args:
            session (Session): session
            user (Commercial | Manager | Technician): The user
        """
        role = session.query(Role).filter_by(id=user.role_id).first()
        self.user_controller.permissions = self.role_permissions.get(role.name)

    def goodbye(self) -> None:
        """
        Method to quit application
        """
        self.view.display_goodbye()
        exit(1)
