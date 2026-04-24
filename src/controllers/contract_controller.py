from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from src.controllers.main_controller import MainController

from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Commercial


class ContractController:
    def __init__(self, main_controller: MainController):
        self.main_controller = main_controller

    def create_contract_with_view(self, session: Session) -> None:
        """
        Method to create contract with view
        Args:
            session (Session): session
        """
        clients = self.main_controller.user_controller.get_models(session=session,
                                                                  model_type="client")

        commercials = self.main_controller.user_controller.get_models(session=session,
                                                                      model_type="commercial")

        (client_id,
         commercial_id,
         total_amount,
         bill_to_pay,
         status
         ) = self.main_controller.view.contract_view.prompt_for_contract(clients=clients,
                                                                         commercials=commercials)
        data ={
            "client_id": client_id,
            "commercial_id": commercial_id,
            "total_amount": total_amount,
            "bill_to_pay": bill_to_pay,
            "status": status
        }
        contract = self.create_contract(session=session, data=data)
        self.main_controller.view.display_action_successfully_done(action="created",
                                                                   model_type="contract")

        contract = self.get_contract(session=session, model_id=contract.id)
        self.main_controller.view.contract_view.display_contract(contract=contract)

    @staticmethod
    def create_contract(session: Session, data: dict) -> Contract:
        """
        Method to create contract
        Args:
            session (Session): session
            data (dict): data

        Returns:
        The contract object
        """
        contract = Contract(client_id=data["client_id"],
                            commercial_id=data["commercial_id"],
                            total_amount=data["total_amount"],
                            bill_to_pay=data["bill_to_pay"],
                            status=data["status"])

        session.add(contract)
        session.commit()
        return contract

    def update_contract_with_view(self, session: Session) -> None:
        """
        Method to update contract with view
        Args:
            session (Session): session
        """
        models = self.main_controller.user_controller.get_models(session=session,
                                                                 model_type="contract")

        self.main_controller.view.display_models(model_type="contract", models=models)

        if models.get("contracts"):
            contract_id = self.main_controller.view.prompt_for_model_id(model_type="contract",
                                                                        models=models.get("contracts"))

            contract = self.get_contract(session=session, model_id=contract_id)
            self.main_controller.view.contract_view.display_contract(contract=contract,)

            self.main_controller.view.display_new_data_request(model_type="contract",
                                                               model_id=contract_id)

            (client_id,
             commercial_id,
             total_amount,
             bill_to_pay,
             status
             ) = self.main_controller.view.contract_view.prompt_for_contract(clients=models.get("clients"),
                                                                             commercials=models.get("commercials"))

            new_contract_data = {
                    "client_id": client_id,
                    "commercial_id": commercial_id,
                    "total_amount": total_amount,
                    "bill_to_pay": bill_to_pay,
                    "status": status
            }
            self.update_contract(session=session, contract_id=contract_id, data=new_contract_data)

            contract = self.get_contract(session=session, model_id=contract_id)

            if contract or (isinstance(contract, list) and (None,) not in contract):
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type="contract")

                self.main_controller.view.contract_view.display_contract(contract=contract)

            else:
                self.main_controller.view.display_something_wrong_while_updating()

    @staticmethod
    def update_contract(session: Session, contract_id: int, data: dict) -> None:
        """
        Method to update contract with view
        Args:
            session (Session): session
            contract_id (int): contract id
            data (dict): data
        """
        session.query(Contract).filter_by(is_active=True, id=contract_id).update(data)
        session.commit()

    def delete_contract(self, session: Session, contract_id: int) -> bool:
        """
        Method to delete contract
        Args:
            session (Session): session
            contract_id (int): contract id

        Returns:
        A boolean indicating if the contract was deleted successfully or not
        """
        events = session.query(Event).filter_by(is_active=True, contract_id=contract_id).first()

        if events or (isinstance(events, list) and (None,) not in events):
            self.main_controller.view.display_cannot_delete(model_type="contract",
                                                            model_linked="event")
            return False

        session.query(Contract).filter_by(is_active=True, id=contract_id).update({"is_active": False})
        session.commit()
        return True

    @staticmethod
    def get_contract(session: Session, model_id: int) -> Contract:
        """
        Method to get contract by its id
        Args:
            session (Session): session
            model_id (int): model id

        Returns:
        A contract object
        """
        contract = session.query(Contract).filter_by(is_active=True, id=model_id).first()
        client = session.query(Client).filter_by(is_active=True, id=contract.client_id).first()
        commercial = session.query(Commercial).filter_by(is_active=True, id=contract.commercial_id).first()
        contract.commercial_name = commercial.name if commercial else ""
        contract.client_name = client.name if client else ""
        contract.client_email = client.email if client else ""
        contract.client_phone = client.phone if client else ""

        return contract

    def filter_contract(self, session: Session,
                        my_filter: str,
                        filter_value: str | int | float | bool,
                        class_name: Contract):
        """
        Method to filter contracts
        Args:
            session (Session): session object
            my_filter (str): filter
            filter_value(str): filter value
            class_name (Contract): Contract object class

        Returns:
        The filtered data for contracts as a list
        """
        results = []
        if my_filter == "client_name":
            results = (session.query(class_name)
                       .join(Client, class_name.client_id == Client.id)
                       .filter(
                class_name.is_active == True, Client.name.contains(filter_value)
            ).all())

        elif my_filter == "status":
            results = session.query(class_name).filter_by(is_active=True, status=filter_value).all()

        elif my_filter == "client_id":
            results = session.query(class_name).filter_by(is_active=True, client_id=filter_value).all()

        elif my_filter == "bill_to_pay" and str(filter_value).isdigit():
            results = session.query(class_name).filter(Contract.is_active == True,
                                                     Contract.bill_to_pay > filter_value).all()

        results = [self.get_contract(session=session, model_id=result.id) for result in results]
        return results
