import bcrypt

from src.database import SessionLocal
from src.models.user import Administrator, Commercial, Technician
from src.seed import admin_credentials


class CollaboratorController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.permissions = None

        self.administrator_controller = AdministratorController(self)
        self.commercial_controller = CommercialController(self)
        self.technician_controller = TechnicianController(self)

    def init_user(self, email, password):
        models = [Commercial, Technician, Administrator]

        session = SessionLocal()
        user = None
        for model in models:
            user = session.query(model).filter_by(email=email, password=password).first()
            if user:
                break

        self.permissions = self.main_controller.role_permissions.get(user.role)
        session.close()

    def init_super_user(self):
        return {
            "name": admin_credentials["name"],
            "email": admin_credentials["email"],
            "password": self.hash_password(admin_credentials["password"]),
            "role": admin_credentials["role"]
        }

    @staticmethod
    def hash_password(password):
        return  bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password, user):
        return bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))

    def login(self):
        while True:
            self.main_controller.view.display_login_submenu()
            menu = self.main_controller.view.prompt_for_continue()

            if menu == 'q':
                break

            email = self.main_controller.view.prompt_for_email()

            models = [Commercial, Technician, Administrator]

            session = SessionLocal()
            user = None
            for model in models:
                user = session.query(model).filter_by(email=email).first()
                if user:
                    break

            if user is None:
                self.main_controller.view.display_collaborator_does_not_exist()
                session.close()
                continue

            password = self.main_controller.view.prompt_for_password()

            if not self.check_password(password, user):
                self.main_controller.view.display_wrong_password()
                session.close()
                continue

            self.authenticate_user(user.name, user.email, user.password)
            # role = user.role.name

            session.close()

            # actions = {
            #     "ADMINISTRATOR": self.administrator_controller.administrator_menu,
            #     "COMMERCIAL": self.commercial_controller.commercial_menu,
            #     "TECHNICIAN": self.technician_controller.technician_menu
            # }
            #
            # action = actions.get(role)
            # action()

    def authenticate_user(self, name, email, password):
        self.init_user(email, password)
        self.main_controller.view.display_successfully_logged_in(name)

    def logout(self):
        self.permissions = None
        self.main_controller.view.display_logout()


class AdministratorController:
    def __init__(self, collaborator_controller):
        self.collaborator_controller = collaborator_controller

    def administrator_menu(self):
        print("Administrator menu")


class CommercialController:
    def __init__(self, collaborator_controller):
        self.collaborator_controller = collaborator_controller

    def commercial_menu(self):
        print("Commercial menu")


class TechnicianController:
    def __init__(self, collaborator_controller):
        self.collaborator_controller = collaborator_controller

    def technician_menu(self):
        print("Technician menu")