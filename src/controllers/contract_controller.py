from src.models.contract import Contract
from src.models.client import Client
from src.models.event import Event
from src.models.user import Commercial


class ContractController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def create_contract_with_view(self, session):
        clients = self.main_controller.user_controller.get_models(session=session, model_type="client")
        commercials = self.main_controller.user_controller.get_models(session=session, model_type="commercial")

        (client_id,
         commercial_id,
         total_amount,
         bill,
         status
         ) = self.main_controller.view.contract_view.prompt_for_contract(clients=clients,
                                                                         commercials=commercials)

        data ={
            "client_id": client_id,
            "commercial_id": commercial_id,
            "total_amount": total_amount,
            "bill": bill,
            "status": status
        }
        contract = self.create_contract(session=session, data=data)

        self.main_controller.view.display_action_successfully_done(action="created",
                                                                   model_type="contract")

        self.main_controller.view.contract_view.display_contract(contract=contract)

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

    def update_contract_with_view(self, session):
        models = self.main_controller.user_controller.get_models(session=session,
                                                                 model_type="contract")

        self.main_controller.view.display_models(model_type="contract", models=models)

        if models.get("contracts"):
            contract_id = self.main_controller.view.prompt_for_model_id(model_type="contract",
                                                                        models=models.get("contracts"))

            contract = self.get_contract(session=session, model_id=contract_id)

            self.main_controller.view.contract_view.display_contract(contract=contract)

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

            if contract and (None,) not in contract:
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type="contract")
                self.main_controller.view.contract_view.display_contract(contract=contract)

            else:
                self.main_controller.view.display_something_wrong_while_updating()

    @staticmethod
    def update_contract(session, contract_id, data):
        session.query(Contract).filter_by(id=contract_id).update(data)
        session.commit()

    def delete_contract(self, session, contract_id):
        events = session.query(Event).filter_by(id=contract_id).first()
        if events and (None,) not in events:
            self.main_controller.view.display_cannot_delete(model_type="contract",
                                                            model_linked="event")
            return

        session.query(Contract).filter_by(id=contract_id).delete()
        session.commit()

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
