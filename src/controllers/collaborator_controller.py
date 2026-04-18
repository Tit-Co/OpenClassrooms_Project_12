from src.database import SessionLocal
from src.models.client import Client
from src.models.event import Event
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Administrator, Commercial, Technician


class CollaboratorController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.permissions = None
        self.models = {
            "contract": Contract,
            "client": Client,
            "event": Event
        }
        self.collaborators = {
            "administrator": Administrator,
            "commercial": Commercial,
            "technician": Technician
        }

    def collaborator_menu(self):
        while True:
            self.main_controller.view.display_collaborator_menu()
            menu = self.main_controller.view.prompt_for_menu(nb=5)

            if menu == 5:
                self.logout()
                break

            actions = {
                1: self.collaborator_submenu,
                2: lambda: self.action_submenu(model_type="Contract", nb=5),
                3: lambda: self.action_submenu(model_type="Client", nb=5),
                4: lambda: self.action_submenu(model_type="Event", nb=5)
            }

            action = actions.get(menu)

            action()

    def collaborator_submenu(self):
        while True:
            self.main_controller.view.display_collaborator_submenu()
            menu = self.main_controller.view.prompt_for_menu(nb=4)

            if menu == 4:
                self.logout()
                break

            actions = {
                1: lambda: self.action_submenu(model_type="Administrator", nb=5),
                2: lambda: self.action_submenu(model_type="Commercial", nb=5),
                3: lambda: self.action_submenu(model_type="Technician", nb=5)
            }

            action = actions.get(menu)

            action()

    def action_submenu(self, model_type, nb):
        while True:
            self.main_controller.view.display_submenu(model_type=model_type)
            menu = self.main_controller.view.prompt_for_menu(nb=nb)

            if menu == 5:
                break

            actions = {
                1: lambda: self.action(action="display", model_type=model_type.lower()),
                2: lambda: self.action(action="create", model_type=model_type.lower()),
                3: lambda: self.action(action="update", model_type=model_type.lower()),
                4: lambda: self.action(action="filter", model_type=model_type.lower()),
            }

            action = actions.get(menu)

            action()

    def action(self, action, model_type):
        if f"{action}:{model_type}" in self.permissions:
            self.main_controller.view.display_action(action, model_type)

            if action == "display":
                models = self.get_models(model_type)

                self.main_controller.view.display_models(model_type=model_type, models=models)

                if models:
                    model_id = self.main_controller.view.prompt_for_model(nb=len(models),
                                                                          action=action,
                                                                          model_type=model_type)

                    model = self.get_model(model_type, model_id)

                    if model_type in self.collaborators.keys():
                        self.main_controller.view.display_collaborator(model)
                    else:
                        self.main_controller.view.display_model(model_type, model)

        else:
            self.main_controller.view.display_permission_denied(action, model_type)

    def get_models(self, model_type):
        session = SessionLocal()
        if model_type in self.models.keys():
            model_class = self.models.get(model_type)
        else:
            model_class = self.collaborators.get(model_type)

        models = session.query(model_class).all()
        session.close()
        return models

    def get_model(self, model_type, model_id):
        session = SessionLocal()
        if model_type in self.models.keys():

            actions = {
                "contract": self.get_contract,
                "client": self.get_client,
                "event": self.get_event,
            }

            action = actions.get(model_type)
            model = action(session, model_id)
        else:
            model = session.query(self.collaborators.get(model_type)).filter_by(id=model_id).first()
            role = session.query(Role).filter_by(id=model.role_id).first()
            model.role_name = role.name
        session.close()
        return model

    @staticmethod
    def get_contract(session, model_id):
        contract = session.query(Contract).filter_by(id=model_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        commercial = session.query(Commercial).filter_by(id=contract.commercial_id).first()
        contract.commercial_name = commercial.name
        contract.client_name = client.name
        contract.client_email = client.email
        contract.client_phone = client.phone

        return contract

    @staticmethod
    def get_client(session, model_id):
        client = session.query(Client).filter_by(id=model_id).first()
        commercial = session.query(Commercial).filter_by(id=client.commercial_id).first()
        client.commercial_name = commercial.name

        return client

    @staticmethod
    def get_event(session, model_id):
        event = session.query(Event).filter_by(id=model_id).first()
        contract = session.query(Contract).filter_by(id=event.contract_id).first()
        technician = session.query(Technician).filter_by(id=event.technician_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        event.client_name = client.name
        event.client_email = client.email
        event.client_phone = client.phone
        event.contract_id = contract.id
        event.technician_name = technician.name

        return event

    def logout(self):
        self.permissions = None
        self.main_controller.view.display_logout()
