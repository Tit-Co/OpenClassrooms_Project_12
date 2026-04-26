from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from src.controllers.main_controller import MainController

from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.role import Role
from src.models.user import Collaborator, Commercial, Manager, Technician


class CollaboratorController:
    def __init__(self, main_controller: MainController):
        self.main_controller = main_controller
        self.permissions = None
        self.current_collaborator = None
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
        self.ROLES_ID = {
            1: Manager,
            2: Commercial,
            3: Technician,
        }

        self.FILTERS = {
            "manager": ["name", "email"],
            "commercial": ["name", "email"],
            "technician": ["name", "email"],
            "contract": ["client-name", "client-id", "creation-date", "status", "bill-to-pay"],
            "client": ["name", "no-commercial", "commercial-id", "commercial-name", "prior-date", "afterward-date"],
            "event": ["name", "location", "attendees-max", "no-technician", "technician-id", "technician-name",
                      "prior-date", "afterward-date"]
        }

    def get_permissions(self, session: Session, user: type[Commercial] | type[Manager] | type[Technician]) -> list:
        role = session.query(Role).filter_by(id=user.role_id).first()

        return self.main_controller.role_permissions.get(role.name)

    def find_user(self, session, email) -> type[Commercial | Manager | Technician]:
        user = self.get_collaborator_by_mail(session, email)
        return user

    def get_current_user(self, session):
        with open("current_user.txt", 'r', encoding="utf-8") as f:
            email = f.read()
            if email:
                return self.get_collaborator_by_mail(session, email)

        return None

    @staticmethod
    def save_current_user(email: str) -> None:
        with open("current_user.txt", 'w', encoding="utf-8") as f:
            f.write(email)

    def reset_current_user(self) -> None:
        self.save_current_user("")

    def collaborator_menu(self, session: Session) -> None:
        """
        Method to launch the collaborator menu.
        Args:
            session (Session): Session object.
        """
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

    def collaborator_submenu(self, session: Session) -> None:
        """
        Method to launch the collaborator submenu.
        Args:
            session (Session): Session object.
        """
        while True:
            self.main_controller.view.display_collaborator_submenu()
            menu = self.main_controller.view.prompt_for_menu(nb=4)

            if menu == 4:
                self.logout(session)
                break

            actions = {
                1: lambda: self.action_submenu(session=session, model_type="Manager", nb=6),
                2: lambda: self.action_submenu(session=session, model_type="Commercial", nb=6),
                3: lambda: self.action_submenu(session=session, model_type="Technician", nb=6),
            }

            action = actions.get(menu)

            action()

    def action_submenu(self, session: Session, model_type: str, nb: int) -> None:
        """
        Method to launch the action submenu.
        Args:
            session (Session): Session object.
            model_type (str): Model type.
            nb (int): Number of actions.
        """
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

    def action(self, session: Session, action: str, model_type: str) -> None:
        """
        Method to launch the action menu.
        Args:
            session (Session): Session object.
            action (str): Action.
            model_type (str): Model type.
        """
        if f"{action}:{model_type}" in self.permissions:
            self.main_controller.view.display_action_introduction(action=action,
                                                                  model_type=model_type)

            actions = {
                "display": self.display_action,
                "create": self.create_action,
                "update": self.update_action,
                "delete": self.delete_action,
                "filter": self.filter_action_with_view,
            }

            action = actions.get(action)
            action(session=session, model_type=model_type)

        else:
            self.main_controller.view.display_permission_denied(action=action,
                                                                model_type=model_type)

    def display_action(self, session: Session, model_type: str) -> None:
        """
        Method to launch display action
        Args:
            session (Session): Session object.
            model_type (str): Model type.
        """
        models = self.get_models(session, model_type)

        self.main_controller.view.display_models(model_type=model_type, models=models)

        if models:
            model_id = self.main_controller.view.prompt_for_model_id_with_action(
                action="display", model_type=model_type, models=models)

            model = self.get_model(session=session, model_type=model_type, model_id=model_id)

            if model_type in self.COLLABORATORS.keys():
                self.main_controller.view.display_collaborator(collaborator=model, role=model_type)
            else:
                self.main_controller.view.display_model(model_type=model_type,
                                                        model=model)

    def create_action(self, session: Session, model_type: str) -> None:
        """
        Method to launch create action
        Args:
            session (Session): Session object.
            model_type (str): Model type.
        """
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

    def create_collaborator_with_view(self, session: Session, role: str) -> None:
        """
        Method to create collaborator with view
        Args:
            session (Session): Session object.
            role (str): Role.
        """
        (email,
         password,
         name) = self.main_controller.view.prompt_for_collaborator(role=role)

        data = {
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }
        collaborator_class = self.COLLABORATORS.get(role)
        requested = self.get_collaborator_by_mail(session=session, email=email)
        inactive = self.get_collaborator_inactive_by_mail(session=session, email=email, role=role)

        if requested:
            self.main_controller.view.display_collaborator_already_exists(collaborator=requested)
            return

        if inactive:
            session.query(collaborator_class).filter_by(is_active=False, email=email).update({"is_active": True})
            self.main_controller.view.display_collaborator_already_exists_but_inactive(collaborator=inactive)
            self.main_controller.view.display_action_successfully_done(action="reactivated",
                                                                       model_type=role)
            collaborator = self.get_collaborator_by_mail(session=session, email=email)
            session.commit()

        else:
            collaborator = self.create_collaborator(session=session, data=data)

            self.main_controller.view.display_action_successfully_done(action="created",
                                                                       model_type=role)

        self.main_controller.view.display_collaborator(collaborator=collaborator, role=role)

    def create_collaborator(self, session: Session, data: dict) -> Manager | Commercial | Technician:
        """
        Method to create collaborator
        Args:
            session (Session): Session object
            data (dict): Data object.

        Returns:
        The collaborator object.
        """
        collaborator = None
        if data["role"] == "manager":
            collaborator = Manager(
                name=data["name"],
                email=data["email"],
                password=self.main_controller.hash_password(password=data["password"]),
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )
        elif data["role"] == "commercial":
            collaborator = Commercial(
                name=data["name"],
                email=data["email"],
                password=self.main_controller.hash_password(password=data["password"]),
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )
        elif data["role"] == "technician":
            collaborator = Technician(
                name=data["name"],
                email=data["email"],
                password=self.main_controller.hash_password(password=data["password"]),
                role_id=session.query(Role).filter_by(name=data["role"].upper()).first().id
            )

        session.add(collaborator)
        session.commit()

        return collaborator

    def update_action(self, session: Session, model_type: str) -> None:
        """
        Method to launch update action
        Args:
            session (Session): Session object.
            model_type (str): Model type.
        """
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


    def update_collaborator_with_view(self, session: Session, role: str) -> None:
        """
        Method to update collaborator with view
        Args:
            session (Session): Session object.
            role (str): Role.
        """
        models = self.get_models(session=session, model_type=role)

        self.main_controller.view.display_models(model_type=role, models=models)

        if models:
            collaborator_id = self.main_controller.view.prompt_for_model_id(model_type=role,
                                                                            models=models)

            collaborator = self.get_collaborator_by_id(session=session,
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

            current_role_id = session.query(Role).filter_by(name=role.upper()).first().id

            if new_role_id != current_role_id:
                new_collaborator_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role": new_role_name,
                }
                new_id = self.change_role_for_collaborator(session=session,
                                                           collaborator_id=collaborator_id,
                                                           current_role=role,
                                                           data=new_collaborator_data)

                collaborator = self.get_collaborator_by_id(session=session,
                                                           collaborator_id=new_id,
                                                           role=new_role_name)

                label = f"collaborator ({role} to {new_role_name})"

            else:
                new_collaborator_data = {
                    "name": name,
                    "email": email,
                    "password": password,
                    "role_id": current_role_id,
                }
                new_role_name = roles[current_role_id]

                self.update_collaborator(session=session,
                                         collaborator_id=collaborator_id,
                                         data=new_collaborator_data)

                collaborator = self.get_collaborator_by_id(session=session,
                                                           collaborator_id=collaborator_id,
                                                           role=new_role_name)
                label = "collaborator"

            if collaborator:
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type=label)

                self.main_controller.view.display_collaborator(collaborator=collaborator,
                                                               role=new_role_name)

            else:
                self.main_controller.view.display_something_wrong("updating")

    def update_collaborator(self, session: Session, collaborator_id: int, data: dict):
        """
        Method to update collaborator
        Args:
            session (Session): Session object.
            collaborator_id (int): Collaborator id.
            data (dict): Collaborator data.
        """
        role_id = data["role_id"]
        name = data["name"]
        email = data["email"]
        password = data["password"]
        role = self.ROLES_ID.get(role_id)

        session.query(role).filter_by(id=collaborator_id).update({"name": name,
                                                                  "email": email,
                                                                  "password": password,
                                                                  "role_id": role_id})
        session.commit()

    def change_role_for_collaborator(self, session: Session,
                                     collaborator_id: int,
                                     current_role: str,
                                     data: dict) -> int:
        """
        Method to change collaborator role
        Args:
            session (Session): Session object.
            collaborator_id (int): Collaborator id.
            current_role (str): Collaborator role.
            data (dict): Collaborator data.

        Returns:
        The collaborator id
        """
        if current_role == "technician":
            session.query(Event).filter(Event.is_active == True, Event.technician_id == collaborator_id)\
                .update({"technician_id": None}, synchronize_session=False)

        elif current_role == "commercial":
            session.query(Contract).filter(Contract.is_active == True, Contract.commercial_id == collaborator_id)\
                .update({"commercial_id": None}, synchronize_session=False)

            session.query(Client).filter(Client.is_active == True, Client.commercial_id == collaborator_id) \
                .update({"commercial_id": None}, synchronize_session=False)

        self.delete_collaborator(session=session,
                                 collaborator_id=collaborator_id,
                                 role=current_role)

        collaborator = self.create_collaborator(session=session, data=data)

        role = data.get("role")
        new_collaborator_id = session.query(self.COLLABORATORS.get(role))\
            .filter_by(is_active=True, id=collaborator.id).first().id

        return new_collaborator_id

    def delete_action(self, session: Session, model_type: str) -> None:
        """
        Method to launch delete action
        Args:
            session (Session): Session object.
            model_type (str): Model type.
        """
        self.delete_model_with_view(session=session, model_type=model_type)

    def filter_action_with_view(self, session: Session, model_type: str) -> None:
        """
        Method to launch filter action
        Args:
            session (Session): Session object.
            model_type (str): Model type.
        """
        filters = self.FILTERS.get(model_type.lower())

        my_filter_id = self.main_controller.view.prompt_for_filter(filters=filters)

        my_filter = self.FILTERS.get(model_type.lower())[my_filter_id - 1]

        if '-id' in my_filter or '-max' in my_filter:
            filter_value = self.main_controller.view.prompt_for_integer(model_type=model_type, my_filter=my_filter)

        elif '-date' in my_filter:
            filter_value = self.main_controller.view.prompt_for_date_filter_value(model_type=model_type, my_filter=my_filter)

        elif 'no-' in my_filter:
            filter_value=None

        elif my_filter == 'status':
            filter_value = self.main_controller.view.contract_view.prompt_for_contract_boolean()

        elif my_filter == 'bill-to-pay':
            filter_value = None

        else:
            filter_value = self.main_controller.view.prompt_for_filter_value(model_type=model_type, my_filter=my_filter)

        results = self.filter_action(session=session,
                                     model_type=model_type,
                                     my_filter=my_filter,
                                     filter_value=filter_value)

        if results:
            self.main_controller.view.display_filter_results(model_type=model_type,
                                                             my_filter=my_filter,
                                                             filter_value=filter_value,
                                                             results=results)
        else:
            self.main_controller.view.display_filter_no_results(model_type=model_type,
                                                                my_filter=my_filter,
                                                                filter_value=filter_value)
    @staticmethod
    def is_float(s: str) -> bool:
        """
        Method that checks if the input is a float
        Args:
            s (str): The input string

        Returns:
        A boolean that indicates if the input is a float or not
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date(s: str) -> bool:
        try:
            s += ':00'
            datetime.strptime(s, "%d/%m/%y %H:%M:%S")
            return True
        except ValueError:
            return False

    @staticmethod
    def is_bool(s: str) -> bool | None:
        if str(s).lower() == "true" or (s.isdigit() and int(s) == 1):
            return True
        elif str(s).lower() == "false" or (s.isdigit() and int(s) == 0):
            return False
        else:
            return None

    def process_filter_value(self, filter_value: str) -> str | int | float | datetime | None:
        """
        Method to process filter value. The method change the type of the filter according to the str input.
        Args:
            filter_value (str): Filter value.

        Returns:
        The processed filter value.
        """
        if filter_value is None or filter_value == '':
            return None

        elif str(filter_value).isdigit():
            return int(filter_value)

        elif self.is_float(str(filter_value)):
            return float(filter_value)

        elif self.is_date(str(filter_value)):
            return datetime.strptime(filter_value, '%d/%m/%y %H:%M:%S')

        elif self.is_bool(str(filter_value)):
            return self.is_bool(filter_value)

        else:
            return filter_value

    def filter_action(self, session: Session,
                      model_type: str,
                      my_filter: str,
                      filter_value: str | int | float | datetime) -> list | None:
        """
        Method to filter data in database by a given filter value
        Args:
            session (Session): Session object.
            model_type (str): Model type.
            my_filter (str): Filter
            filter_value (str | int | float | datetime): Filter value

        Returns:
        The filtered data
        """
        class_name = self.MODELS.get(model_type) if self.MODELS.get(model_type) \
            else self.COLLABORATORS.get(model_type)

        filter_value = self.process_filter_value(filter_value)

        results = []

        if model_type in self.COLLABORATORS.keys():
            results = self.filter_collaborator(session=session,
                                               model_type=model_type,
                                               my_filter=my_filter,
                                               filter_value=filter_value,
                                               class_name=class_name)

        elif model_type in self.MODELS.keys():
            actions = {
                "contract": self.main_controller.contract_controller.filter_contract,

                "client": self.main_controller.client_controller.filter_client,

                "event": self.main_controller.event_controller.filter_event
            }
            action = actions.get(model_type)
            results = action(session=session, my_filter=my_filter, filter_value=filter_value, class_name=class_name)

        return results

    def filter_collaborator(self, session: Session,
                            model_type: str,
                            my_filter: str,
                            filter_value: str | int | float | datetime,
                            class_name: Commercial | Manager | Technician) -> list | None:
        """
        Method to filter collaborators
        Args:
            session (Session): Session object.
            model_type (str): Model type.
            my_filter (str): Filter
            filter_value (str | int | float | datetime): Filter value
            class_name (Commercial | Manager | Technician): Collaborator

        Returns:
        The filtered data as a list
        """
        results = []
        if my_filter == "name":
            results = session.query(class_name).filter(class_name.is_active == True,
                                                       class_name.name.contains(filter_value)).all()

        elif my_filter == "email":
            results = session.query(class_name).filter(class_name.is_active == True,
                                                       class_name.email.contains(filter_value)).all()

        results = [self.get_collaborator_by_id(session=session, role=model_type, collaborator_id=result.id)
                   for result in results]

        return results


    def get_models(self, session: Session, model_type: str) -> dict | list:
        """
        Methods to get all models of a type and in case of contracts, some extra data are added
        and a dict is returned
        Args:
            session (Session): Session object.
            model_type (str): Model type.

        Returns:
        The list of models or a dictionary with contracts list and extra data.
        """
        if model_type in self.MODELS.keys():
            if model_type == "contract":
                models={
                    "contracts": session.query(self.MODELS.get("contract")).filter_by(is_active=True).all(),
                    "clients": session.query(self.MODELS.get("client")).filter_by(is_active=True).all(),
                    "commercials": session.query(self.COLLABORATORS.get("commercial")).filter_by(is_active=True).all()
                }
                return models
            else:
                model_class = self.MODELS.get(model_type)
        else:
            model_class = self.COLLABORATORS.get(model_type)
        models = session.query(model_class).filter_by(is_active=True).all()
        return models

    def get_object_by_id(self, session: Session, model_type: str, object_id: int) -> (type[Client | Event | Contract]):
        """
        Method to get an object of class Contract, Client or Event according to the given id and type
        Args:
            session (Session): Session object.
            model_type (str): Model type.
            object_id (int): Object id.

        Returns:
        The object found.
        """
        actions = {
            "contract": self.main_controller.contract_controller.get_contract,
            "client": self.main_controller.client_controller.get_client,
            "event": self.main_controller.event_controller.get_event,
        }

        action = actions.get(model_type)
        my_object = action(session=session, model_id=object_id)

        return my_object

    def get_model(self, session: Session,
                  model_type: str,
                  model_id: int) -> (type[Client | Event | Contract | Commercial | Manager | Technician]):
        """
        Method to get a model by its id and type
        Args:
            session (Session): Session object.
            model_type (str): Model type
            model_id (int): Model id.

        Returns:
        The model as Event or Client or Contract.
        """
        model = None
        if model_type in self.MODELS.keys():
            model=self.get_object_by_id(session=session, model_type=model_type, object_id=model_id)

        elif model_type in self.COLLABORATORS.keys():
            model = self.get_collaborator_by_id(session=session, collaborator_id=model_id, role=model_type)
            role = session.query(Role).filter_by(id=model.role_id).first()
            model.role_name = role.name

        return model

    def get_collaborator_by_id(self, session: Session, collaborator_id: int, role: str) -> type[Collaborator]:
        """
        Method to get a collaborator by its id
        Args:
            session (Session): Session object
            collaborator_id (int): Collaborator id.
            role (str): Collaborator role.

        Returns:
        The collaborator object as Commercial or Manager or Technician.
        """
        collaborator_class = self.COLLABORATORS.get(role)
        collaborator = session.query(collaborator_class).filter_by(is_active=True, id=collaborator_id).first()

        return collaborator

    @staticmethod
    def get_collaborator_by_mail(session: Session, email: str) -> type[Commercial | Manager | Technician] | None:
        """
        Method to get a collaborator by its email
        Args:
            session (Session): Session object
            email (str): Collaborator e-mail.

        Returns:
        The collaborator object as Commercial or Manager or Technician.
        """
        collaborator = session.query(Manager).filter_by(is_active=True, email=email).first()

        if collaborator:
            return collaborator

        collaborator = session.query(Commercial).filter_by(is_active=True, email=email).first()
        if collaborator:
            return collaborator

        return session.query(Technician).filter_by(is_active=True, email=email).first()

    def get_collaborator_inactive_by_mail(self, session: Session, email: str, role: str) -> type[Collaborator]:
        """
        Method to get an inactive collaborator by its name
        Args:
            session (Session): Session object
            collaborator_email (str): Collaborator e-mail.
            role (str): Collaborator role.

        Returns:
        The collaborator object as Commercial or Manager or Technician.
        """
        collaborator_class = self.COLLABORATORS.get(role)
        collaborator = session.query(collaborator_class).filter_by(is_active=False, email=email).first()

        return collaborator

    @staticmethod
    def get_admin(session: Session) -> type[Manager]:
        """
        Method to get the admin
        Args:
            session (Session): Session object.

        Returns:
        The admin manager object.
        """
        return session.query(Manager).filter_by(is_active=True, id=1).first()

    def delete_model_with_view(self, session: Session, model_type: str) -> None:
        """
        Method to launch delete action with view by type of model
        Args:
            session (Session): Session object.
            model_type (str): Model type.

        Returns:
        None
        """
        models = self.main_controller.user_controller.get_models(session=session,
                                                                 model_type=model_type)
        models = models.get(model_type) if model_type=="contract" else models

        if models:
            self.main_controller.view.display_models(model_type=model_type, models=models)

            model_id = self.main_controller.view.prompt_for_model_id(model_type=model_type,
                                                                     models=models)
            admin = self.get_admin(session=session)

            requested = self.get_model(session=session, model_id=model_id, model_type=model_type)

            if admin == requested or requested == self.current_collaborator:
                self.main_controller.view.display_cannot_delete_admin_manager_or_yourself()
                return

            if not self.main_controller.view.prompt_for_confirmation(action="delete",
                                                                     model_type=model_type):
                return

            delete_actions = {
                "contract": lambda : self.main_controller.contract_controller\
                    .delete_contract(session=session, contract_id=model_id),

                "client": lambda : self.main_controller.client_controller\
                    .delete_client(session=session, client_id=model_id),

                "event": lambda : self.main_controller.event_controller\
                    .delete_event(session=session, event_id=model_id),

                "manager": lambda : self.main_controller.user_controller\
                    .delete_collaborator(session=session, collaborator_id=model_id, role=model_type),

                "commercial": lambda : self.main_controller.user_controller\
                    .delete_collaborator(session=session, collaborator_id=model_id, role=model_type),

                "technician": lambda : self.main_controller.user_controller\
                    .delete_collaborator(session=session, collaborator_id=model_id, role=model_type)
            }
            action = delete_actions.get(model_type)
            success = action()

            if success:
                self.main_controller.view.display_action_successfully_done(action="deleted",
                                                                           model_type=model_type)
        else:
            self.main_controller.view.display_action_impossible(action="delete")

    def delete_collaborator(self, session: Session, collaborator_id: int, role: str) -> bool:
        """
        Method to delete collaborator by its id
        Args:
            session (Session): Session object.
            collaborator_id (int): Collaborator id.
            role (str): Collaborator role.

        Returns:
        A boolean indicating whether deletion was successful.
        """
        # if role == "commercial":
        #     clients = session.query(Client).filter_by(commercial_id=collaborator_id).all()
        #
        #     if clients:
        #         self.main_controller.view.display_cannot_delete(model_type=role,
        #                                                         model_linked="client")
        #         return False

        try:
            session.query(self.COLLABORATORS.get(role)).filter_by(is_active=True, id=collaborator_id)\
                .update({"is_active": False})
            session.commit()
            return True

        except Exception:
            self.main_controller.view.display_something_wrong("deleting")
            return False

    def model_exists(self, session: Session, model_type: str, value: str) -> bool:
        """
        Method to check if a model exists by its type and its value
        Args:
            session (Session): Session object.
            model_type (str): Model type.
            value (str): Model value.

        Returns:
        A boolean indicating whether model exists.
        """
        result = None
        if model_type == "client":
            result = session.query(self.MODELS[model_type]).filter_by(is_active=True, email=value).first()

        elif model_type == "event":
            class_name = self.MODELS[model_type]
            result = session.query(class_name).filter_by(is_active=True, name=value).first()

        return result is not None or (isinstance(result, list) and (None,) not in result)

    def logout(self, session: Session) -> None:
        """
        Method to log out a user from a session
        Args:
            session (Session): Session object.
        """
        session.close()
        self.reset_current_user()
        self.permissions = None
        self.main_controller.view.display_logout()
