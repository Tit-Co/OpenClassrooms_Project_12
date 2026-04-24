from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from src.controllers.main_controller import MainController

from src.models.client import Client
from src.models.contract import Contract
from src.models.user import Commercial


class ClientController:
    def __init__(self, main_controller: MainController):
        self.main_controller = main_controller

    def create_client_with_view(self, session: Session) -> None:
        """
        Method to create client with view
        Args:
            session (SessionLocal): Session instance
        """
        commercials = self.main_controller.user_controller.get_models(session=session, model_type="commercial")

        (commercial_id,
         name,
         email,
         phone,
         company
         ) = self.main_controller.view.client_view.prompt_for_client(commercials=commercials)

        if not self.main_controller.user_controller.model_exists(session=session,
                                                                 model_type="client",
                                                                 value=email):
            data = {
                "commercial_id": commercial_id,
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "creation_date": datetime.now(),
                "last_update": datetime.now(),
            }
            client = self.create_client(session=session, data=data)

            self.main_controller.view.display_action_successfully_done(action="created",
                                                                       model_type="client")

            client = self.get_client(session=session, model_id=client.id)
            self.main_controller.view.client_view.display_client(client=client)
        else:
            self.main_controller.view.display_model_already_exist(model_type="client")

    @staticmethod
    def create_client(session: Session, data: dict) -> Client:
        """
        Method to create client
        Args:
            session (SessionLocal): Session instance
            data (dict): data

        Returns:
        The created client object
        """
        client = Client(commercial_id=data["commercial_id"],
                          name=data["name"],
                          email=data["email"],
                          phone=data["phone"],
                          company=data["company"],
                          creation_date=data["creation_date"],
                          last_update=data["last_update"])

        session.add(client)
        session.commit()
        return client

    def update_client_with_view(self, session: Session) -> None:
        """
        Method to update client with view
        Args:
            session (SessionLocal): Session instance
        """
        clients = self.main_controller.user_controller.get_models(session=session, model_type="client")
        commercials = self.main_controller.user_controller.get_models(session=session, model_type="commercial")

        self.main_controller.view.display_models(model_type="client", models=clients)

        if clients:
            client_id = self.main_controller.view.prompt_for_model_id(model_type="client",
                                                                      models=clients)

            client = self.get_client(session=session, model_id=client_id)
            creation_date = client.creation_date

            self.main_controller.view.client_view.display_client(client=client)

            self.main_controller.view.display_new_data_request(model_type="client",
                                                               model_id=client_id)

            (commercial_id,
             name,
             email,
             phone,
             company,
             ) = self.main_controller.view.client_view.prompt_for_client(commercials=commercials)

            new_contract_data = {
                "commercial_id": commercial_id,
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "creation_date": creation_date,
                "last_update": datetime.now(),
            }

            self.update_client(session=session, client_id=client_id, data=new_contract_data)

            client = self.get_client(session=session, model_id=client_id)

            if client:
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type="client")


                self.main_controller.view.client_view.display_client(client=client)
            else:
                self.main_controller.view.display_something_wrong_while_updating()

    @staticmethod
    def update_client(session: Session, client_id: int, data: dict) -> None:
        """
        Method to update client with view
        Args:
            session (SessionLocal): Session instance
            client_id (int): Client id
            data (dict): data
        """
        session.query(Client).filter_by(is_active=True, id=client_id).update(data)
        session.commit()

    def delete_client(self, session: Session, client_id: int) -> bool:
        """
        Method to delete client with view
        Args:
            session (SessionLocal): Session instance
            client_id (int): Client id

        Returns:
        A boolean indicating if the client was deleted successfully or not
        """
        client = session.query(Contract).filter_by(is_active=True, client_id=client_id).first()
        if client:
            self.main_controller.view.display_cannot_delete(model_type="client",
                                                            model_linked="contract")
            return False

        session.query(Client).filter_by(is_active=True, id=client_id).delete()
        session.commit()
        return True

    @staticmethod
    def get_client(session: Session, model_id: int) -> Client:
        """
        Method to get client and add fields for extra data
        Args:
            session (SessionLocal): Session instance
            model_id (int): Client id

        Returns:
        The client object
        """
        client = session.query(Client).filter_by(is_active=True, id=model_id).first()
        commercial = session.query(Commercial).filter_by(is_active=True, id=client.commercial_id).first()
        client.commercial_name = commercial.name if commercial else ""

        return client

    def filter_client(self, session: Session,
                      my_filter: str,
                      filter_value: str | int | float | datetime,
                      class_name: Client) -> list:
        """
        Method to filter clients
        Args:
            session (Session): Session object
            my_filter (str): Filter
            filter_value(str | int | float | datetime): Filter value.
            class_name (Client): Client object

        Returns:
        The filtered data for clients as a list
        """
        results = []
        if my_filter == "name":
            results = (session.query(class_name)
                       .filter(class_name.is_active == True,
                               class_name.name.contains(filter_value)).all())

        elif my_filter == "no_commercial":
            results = session.query(class_name).filter_by(is_active=True, commercial_id=None).all()

        elif my_filter == "commercial_id":
            results = session.query(class_name).filter_by(is_active=True, commercial_id=filter_value).all()

        elif my_filter == "commercial_name":
            results = (session.query(class_name)
                       .join(Commercial, class_name.commercial_id == Commercial.id)
                       .filter(
                class_name.is_active == True, Commercial.name.contains(filter_value)
            ).all())

        elif my_filter == "prior_date":
            results = (
                session.query(class_name)
                .filter(
                    class_name.is_active == True,
                    class_name.last_update < filter_value
                )
                .all()
            )

        elif my_filter == "afterward_date":
            results = (
                session.query(class_name)
                .filter(
                    class_name.is_active == True,
                    class_name.last_update > filter_value
                )
                .all()
            )
        results = [self.get_client(session=session, model_id=result.id) for result in results]
        return results
