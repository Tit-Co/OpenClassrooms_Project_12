from src.models.client import Client
from src.models.event import Event
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Manager, Commercial, Technician


class CollaboratorController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.permissions = None
        self.MODELS = {
            "contract": Contract,
            "client": Client,
            "event": Event
        }
        self.COLLABORATORS = {
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
            self.main_controller.view.display_action_introduction(action=action,
                                                                  model_type=model_type)

            actions = {
                "display": self.display_action,
                "create": self.create_action,
                "update": self.update_action,
                "delete": self.delete_action,
                "filter": self.filter_action,
            }

            action = actions.get(action)
            action(session=session, model_type=model_type)

        else:
            self.main_controller.view.display_permission_denied(action=action,
                                                                model_type=model_type)

    def display_action(self, session, model_type):
        models = self.get_models(session, model_type)

        self.main_controller.view.display_models(model_type=model_type, models=models)

        if models:
            model_id = self.main_controller.view.prompt_for_model_id_with_action(
                action="display", model_type=model_type, models=models)

            model = self.get_model(session=session, model_type=model_type, model_id=model_id)

            if model_type in self.COLLABORATORS.keys():
                self.main_controller.view.display_collaborator(collaborator=model, role=model_type)
            else:
                if model_type == "event":
                    add_on = self.main_controller.event_controller.get_event_add_on(session=session,
                                                                                    event=model)
                    self.main_controller.view.event_view.display_event(event=model, add_on=add_on)
                else:
                    self.main_controller.view.display_other_model(model_type=model_type,
                                                                  model=model)

    def create_action(self, session, model_type):
        actions = {
            "contract": lambda: self.main_controller.contract_controller.create_contract_with_view(session=session),
            "client": lambda: self.main_controller.client_controller.create_client_with_view(session=session),
            "event": lambda: self.main_controller.event_controller.create_event_with_view(session=session),
            "manager": lambda: self.create_collaborator_with_view(session=session, role=model_type),
            "commercial": lambda: self.create_collaborator_with_view(session=session, role=model_type),
            "technician": lambda: self.create_collaborator_with_view(session=session, role=model_type)
        }
        action = actions.get(model_type)
        action()

    def create_collaborator_with_view(self, session, role):
        (email,
         password,
         name) = self.main_controller.view.prompt_for_collaborator(role=role)

        data = {
            "name": name,
            "email": email,
            "password": self.main_controller.hash_password(password=password),
            "role": role
        }

        collaborator = self.create_collaborator(session=session, data=data)

        self.main_controller.view.display_action_successfully_done(action="created",
                                                                   model_type=role)

        self.main_controller.view.display_collaborator(collaborator=collaborator, role=role)

    @staticmethod
    def create_collaborator(session, data):
        collaborator = None
        if data["role"] == "manager":
            collaborator = Manager(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )
        elif data["role"] == "commercial":
            collaborator = Commercial(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )
        elif data["role"] == "technician":
            collaborator = Technician(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )

        session.add(collaborator)
        session.commit()

        return collaborator

    def update_action(self, session, model_type):
        actions = {
            "contract": lambda: self.main_controller.contract_controller.update_contract_with_view(session=session),
            "client": lambda: self.main_controller.client_controller.update_client_with_view(session=session),
            "event": lambda: self.main_controller.event_controller.update_event_with_view(session=session),
            "manager": lambda: self.update_collaborator_with_view(session=session, role=model_type),
            "commercial": lambda: self.update_collaborator_with_view(session=session, role=model_type),
            "technician": lambda: self.update_collaborator_with_view(session=session, role=model_type)
        }
        action = actions.get(model_type)
        action()


    def update_collaborator_with_view(self, session, role):
        models = self.get_models(session=session, model_type=role)

        self.main_controller.view.display_models(model_type=role, models=models)

        if models:
            collaborator_id = self.main_controller.view.prompt_for_model_id(model_type=role,
                                                                            models=models)

            collaborator = self.get_collaborator(session=session,
                                                 collaborator_id=collaborator_id,
                                                 role=role)

            self.main_controller.view.display_collaborator(collaborator=collaborator, role=role)

            self.main_controller.view.display_new_data_request(model_type=role,
                                                               model_id=collaborator_id)

            (email,
             password,
             name) = self.main_controller.view.prompt_for_collaborator(role=role)

            roles = {
                1: "manager",
                2: "commercial",
                3: "technician",
            }
            new_role_id, new_role_name = self.main_controller.view.prompt_for_collaborator_role(roles=roles)

            current_role_id = session.query(Role).filter_by(name=role).first().id

            if new_role_id != current_role_id:
                new_collaborator_data = {
                    "name": name,
                    "email": email,
                    "password": self.main_controller.hash_password(password=password),
                    "role": new_role_name,
                }
                new_id = self.change_role_for_collaborator(session=session,
                                                           collaborator_id=collaborator_id,
                                                           current_role=role,
                                                           data=new_collaborator_data)

                collaborator = self.get_collaborator(session=session,
                                                     collaborator_id=new_id,
                                                     role=new_role_name)

            else:
                new_collaborator_data = {
                    "name": name,
                    "email": email,
                    "password": self.main_controller.hash_password(password=password),
                    "role_id": current_role_id,
                }
                new_role_name = roles[current_role_id]

                self.update_collaborator(session=session,
                                         collaborator_id=collaborator_id,
                                         data=new_collaborator_data)

                collaborator = self.get_collaborator(session=session,
                                                     collaborator_id=collaborator_id,
                                                     role=new_role_name)

            if collaborator:
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type="collaborator")

                self.main_controller.view.display_collaborator(collaborator=collaborator,
                                                               role=new_role_name)

            else:
                self.main_controller.view.display_something_wrong_while_updating()

    def update_collaborator(self, session, collaborator_id, data):
        session.query(self.MODELS.get(data["role"])).filter_by(id=collaborator_id).update(data=data)

        session.commit()

    def change_role_for_collaborator(self, session, collaborator_id, current_role, data):
        if current_role == "technician":
            session.query(Event).filter(Event.technician_id == collaborator_id)\
                .update({"technician_id": None}, synchronize_session=False)

        elif current_role == "commercial":
            session.query(Contract).filter(Contract.commercial_id == collaborator_id)\
                .update({"commercial_id": None}, synchronize_session=False)

            session.query(Client).filter(Client.commercial_id == collaborator_id) \
                .update({"commercial_id": None}, synchronize_session=False)

        self.delete_collaborator(session=session,
                                 collaborator_id=collaborator_id,
                                 role=current_role)

        collaborator = self.create_collaborator(session=session, data=data)

        role = data.get("role")
        new_collaborator_id = session.query(self.COLLABORATORS.get(role))\
            .filter_by(id=collaborator.id).first().id

        return new_collaborator_id

    def delete_action(self, session, model_type):
        self.delete_model_with_view(session=session, model_type=model_type)

    def filter_action(self, session, model_type):
        pass

    def get_models(self, session, model_type):
        if model_type in self.MODELS.keys():
            if model_type == "contract":
                models={
                    "contracts": session.query(self.MODELS.get("contract")).all(),
                    "clients": session.query(self.MODELS.get("client")).all(),
                    "commercials": session.query(self.COLLABORATORS.get("commercial")).all()
                }
                return models
            else:
                model_class = self.MODELS.get(model_type)
        else:
            model_class = self.COLLABORATORS.get(model_type)
        models = session.query(model_class).all()

        return models

    def get_model(self, session, model_type, model_id):
        model = None
        if model_type in self.MODELS.keys():

            actions = {
                "contract": self.main_controller.contract_controller.get_contract,
                "client": self.get_client,
                "event": self.get_event,
            }

            action = actions.get(model_type)
            model = action(session=session, model_id=model_id)

        elif model_type in self.COLLABORATORS.keys():
            model = self.get_collaborator(session=session, collaborator_id=model_id, role=model_type)
            role = session.query(Role).filter_by(id=model.role_id).first()
            model.role_name = role.name

        return model

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

    def get_collaborator(self, session, collaborator_id, role):
        collaborator_class = self.COLLABORATORS.get(role)
        collaborator = session.query(collaborator_class).filter_by(id=collaborator_id).first()

        return collaborator

    def delete_model_with_view(self, session, model_type):
        models = self.main_controller.main_controller.get_models(session=session, model_type=model_type)

        self.main_controller.view.display_models(model_type=model_type, models=models)

        if models:
            model_id = self.main_controller.view.prompt_for_model_id(model_type=model_type,
                                                                      models=models)

            if self.main_controller.view.prompt_for_confirmation(action="delete",
                                                                 model_type=model_type):

                delete_actions = {
                    "contract": self.main_controller.contract_controller.delete_contract,
                    "client": self.main_controller.client_controller.delete_client,
                    "event": self.main_controller.event_controller.delete_event,
                    "manager": lambda : self.main_controller.delete_collaborator(role=model_type),
                    "commercial": lambda : self.main_controller.delete_collaborator(role=model_type),
                    "technician": lambda : self.main_controller.delete_collaborator(role=model_type)
                }
                action = delete_actions.get(model_type)
                action(session=session, event_id=model_id)

                self.main_controller.view.display_action_successfully_done(action="deleted",
                                                                           model_type=model_type)

    def delete_collaborator(self, session, collaborator_id, role):
        session.query(self.COLLABORATORS.get(role)).filter_by(id=collaborator_id).delete()
        session.commit()

    def model_exists(self, session, model_type, value):
        query = None
        if model_type == "client":
            query = session.query(self.MODELS[model_type]).filter_by(email=value).first()

        elif model_type == "event":
            query = session.query(self.MODELS[model_type]).filter_by(name=value).first()

        return query is not None or (isinstance(query, list) and (None,) not in query)

    def logout(self, session):
        session.close()
        self.permissions = None
        self.main_controller.view.display_logout()
