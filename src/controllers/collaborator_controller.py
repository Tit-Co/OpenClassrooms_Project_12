from src.models.client import Client
from src.models.event import Event
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Manager, Commercial, Technician


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
            "manager": Manager,
            "commercial": Commercial,
            "technician": Technician
        }

    def collaborator_menu(self, session):
        while True:
            self.main_controller.view.display_collaborator_menu()
            menu = self.main_controller.view.prompt_for_menu(nb=5)

            if menu == 5:
                self.logout(session)
                break

            actions = {
                1: lambda : self.collaborator_submenu(session=session),
                2: lambda: self.action_submenu(session=session, model_type="Contract", nb=6),
                3: lambda: self.action_submenu(session=session, model_type="Client", nb=6),
                4: lambda: self.action_submenu(session=session, model_type="Event", nb=6)
            }

            action = actions.get(menu)

            action()

    def collaborator_submenu(self, session):
        while True:
            self.main_controller.view.display_collaborator_submenu()
            menu = self.main_controller.view.prompt_for_menu(nb=4)

            if menu == 4:
                self.logout(session)
                break

            actions = {
                1: lambda: self.action_submenu(session=session, model_type="Manager", nb=6),
                2: lambda: self.action_submenu(session=session, model_type="Commercial", nb=6),
                3: lambda: self.action_submenu(session=session, model_type="Technician", nb=6)
            }

            action = actions.get(menu)

            action()

    def action_submenu(self, session, model_type, nb):
        while True:
            self.main_controller.view.display_submenu(model_type=model_type)
            menu = self.main_controller.view.prompt_for_menu(nb=nb)

            if menu == 6:
                break

            actions = {
                1: lambda: self.action(session=session, action="display", model_type=model_type.lower()),
                2: lambda: self.action(session=session, action="create", model_type=model_type.lower()),
                3: lambda: self.action(session=session, action="update", model_type=model_type.lower()),
                4: lambda: self.action(session=session, action="delete", model_type=model_type.lower()),
                5: lambda: self.action(session=session, action="filter", model_type=model_type.lower()),
            }

            action = actions.get(menu)

            action()

    def action(self, session, action, model_type):
        if f"{action}:{model_type}" in self.permissions:
            self.main_controller.view.display_action(action, model_type)

            actions = {
                "display": lambda: self.display_action(session=session, model_type=model_type),
                "create": lambda: self.create_action(session=session, model_type=model_type),
                "update": lambda: self.update_action(session=session, model_type=model_type),
                "delete": lambda: self.delete_action(session=session, model_type=model_type),
                "filter": lambda: self.filter_action(session=session, model_type=model_type),
            }

            action = actions.get(action)
            action()

        else:
            self.main_controller.view.display_permission_denied(action, model_type)

    def display_action(self, session, model_type):
        models = self.get_models(session, model_type)

        self.main_controller.view.display_models(model_type=model_type, models=models)

        if models:
            model_id = self.main_controller.view.prompt_for_model_id_with_action(
                action="display", model_type=model_type, models=models)

            model = self.get_model(session, model_type, model_id)

            if model_type in self.collaborators.keys():
                self.main_controller.view.display_collaborator(model)
            else:
                self.main_controller.view.display_model(model_type, model)

    def create_action(self, session, model_type):
        actions = {
            "contract": lambda: self.create_contract_with_view(session=session),
            "client": lambda: self.create_client(session=session),
            "event": lambda: self.create_event(session=session),
            "manager": lambda: self.create_collaborator(session=session, role=model_type),
            "commercial": lambda: self.create_collaborator(session=session, role=model_type),
            "technician": lambda: self.create_collaborator(session=session, role=model_type)
        }
        action = actions.get(model_type)
        action()

    def create_contract_with_view(self, session):
        clients = self.get_models(session=session, model_type="client")
        commercials = self.get_models(session=session, model_type="commercial")

        (client_id,
         commercial_id,
         total_amount,
         bill,
         status
         ) = self.main_controller.view.contract_view.prompt_for_contract(clients, commercials)

        data ={
            "client_id": client_id,
            "commercial_id": commercial_id,
            "total_amount": total_amount,
            "bill": bill,
            "status": status
        }
        contract = self.create_contract(session, data)

        self.main_controller.view.display_action_successfully_done(action="created",
                                                                   model_type="contract")
        self.main_controller.view.contract_view.display_contract(
            contract=self.get_model(session=session, model_type="contract", model_id=contract.id))

    @staticmethod
    def create_contract(session, data):
        contract = Contract(client_id=data["client_id"],
                            commercial_id=data["commercial_id"],
                            total_amount=data["total_amount"],
                            bill_to_pay=data["bill"],
                            status=data["status"])

        session.add(contract)
        session.commit()
        return contract

    def create_client(self, session):
        pass

    def create_event(self, session):
        pass

    def create_collaborator(self, session, role):
        pass

    def update_action(self, session, model_type):
        actions = {
            "contract": lambda: self.update_contract_with_view(session=session),
            "client": lambda: self.update_client(session=session),
            "event": lambda: self.update_event(session=session),
            "manager": lambda: self.update_collaborator(session=session, role=model_type),
            "commercial": lambda: self.update_collaborator(session=session, role=model_type),
            "technician": lambda: self.update_collaborator(session=session, role=model_type)
        }
        action = actions.get(model_type)
        action()

    def update_contract_with_view(self, session):
        clients = self.get_models(session=session, model_type="client")
        commercials = self.get_models(session=session, model_type="commercial")
        contracts = self.get_models(session=session, model_type="contract")

        self.main_controller.view.display_models(model_type="contract", models=contracts)

        if contracts:
            contract_id = self.main_controller.view.prompt_for_model_id(model_type="contract",
                                                                        models=contracts)

            contract = self.get_contract(session=session, model_id=contract_id)

            self.main_controller.view.display_title(model_type="contract")
            self.main_controller.view.contract_view.display_contract(contract=contract)

            self.main_controller.view.display_new_data_request(model_type="contract",
                                                               model_id=contract_id)

            (client_id,
             commercial_id,
             total_amount,
             bill_to_pay,
             status
             ) = self.main_controller.view.contract_view.prompt_for_contract(clients, commercials)

            new_contract_data = {
                    "client_id": client_id,
                    "commercial_id": commercial_id,
                    "total_amount": total_amount,
                    "bill_to_pay": bill_to_pay,
                    "status": status
            }
            self.update_contract(session=session, contract_id=contract_id, data=new_contract_data)

            contract = self.get_contract(session=session, model_id=contract_id)
            self.main_controller.view.display_title(model_type="new contract")
            self.main_controller.view.display_action_successfully_done(action="updated",
                                                                       model_type="contract")
            self.main_controller.view.contract_view.display_contract(contract=contract)

    @staticmethod
    def update_contract(session, contract_id, data):
        session.query(Contract).filter_by(id=contract_id).update(data)
        session.commit()

    def update_client(self, session):
        pass

    def update_event(self, session):
        pass

    def update_collaborator(self, session):
        pass

    def delete_action(self, session, model_type):
        actions = {
            "contract": lambda: self.delete_contract_with_view(session=session),
            "client": lambda: self.delete_client(session=session),
            "event": lambda: self.delete_event(session=session),
            "manager": lambda: self.delete_collaborator(session=session, role=model_type),
            "commercial": lambda: self.delete_collaborator(session=session, role=model_type),
            "technician": lambda: self.delete_collaborator(session=session, role=model_type)
        }
        action = actions.get(model_type)
        action()

    def delete_contract_with_view(self, session):
        contracts = self.get_models(session=session, model_type="contract")

        self.main_controller.view.display_models(model_type="contract", models=contracts)

        if contracts:
            contract_id = self.main_controller.view.prompt_for_model_id(model_type="contract",
                                                                        models=contracts)

            if self.main_controller.view.prompt_for_confirmation(action="delete",
                                                                 model_type="contract"):
                self.delete_contract(session=session, contract_id=contract_id)

                self.main_controller.view.display_action_successfully_done(action="deleted",
                                                                           model_type="contract")

    @staticmethod
    def delete_contract(session, contract_id):
        session.query(Contract).filter_by(id=contract_id).delete()
        session.commit()

    def filter_action(self, session, model_type):
        pass

    def get_models(self, session, model_type):
        if model_type in self.models.keys():
            model_class = self.models.get(model_type)
        else:
            model_class = self.collaborators.get(model_type)

        models = session.query(model_class).all()

        return models

    def get_model(self, session, model_type, model_id):
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

        return model

    @staticmethod
    def get_contract(session, model_id):
        contract = session.query(Contract).filter_by(id=model_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        commercial = session.query(Commercial).filter_by(id=contract.commercial_id).first()
        contract.commercial_name = commercial.name if commercial else ""
        contract.client_name = client.name if client else ""
        contract.client_email = client.email if client else ""
        contract.client_phone = client.phone if client else ""

        return contract

    @staticmethod
    def get_client(session, model_id):
        client = session.query(Client).filter_by(id=model_id).first()
        commercial = session.query(Commercial).filter_by(id=client.commercial_id).first()
        client.commercial_name = commercial.name if commercial else ""

        return client

    @staticmethod
    def get_event(session, model_id):
        event = session.query(Event).filter_by(id=model_id).first()
        contract = session.query(Contract).filter_by(id=event.contract_id).first()
        technician = session.query(Technician).filter_by(id=event.technician_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        event.client_name = client.name if client else ""
        event.client_email = client.email if client else ""
        event.client_phone = client.phone if client else ""
        event.contract_id = contract.id if contract else ""
        event.technician_name = technician.name if technician else ""

        return event

    def logout(self, session):
        session.close()
        self.permissions = None
        self.main_controller.view.display_logout()
