from src.models.contract import Contract
from src.models.client import Client
from src.models.event import Event
from src.models.user import Commercial


class ContractController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    @staticmethod
    def get_contract_add_on(session, contract):
        client = session.query(Client).filter(Client.id==contract.client_id).first()
        commercial = session.query(Commercial).filter(Commercial.id==contract.commercial_id).first()

        add_on = {
        "client_name": client.name,
        "client_phone": client.phone,
        "client_email": client.email,
        "commercial_name": commercial.name
        }
        return add_on

    def create_contract_with_view(self, session):
        clients = self.main_controller.user_controller.get_models(session=session, model_type="client")
        commercials = self.main_controller.user_controller.get_models(session=session, model_type="commercial")

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
    def create_contract(session, data):
        contract = Contract(client_id=data["client_id"],
                            commercial_id=data["commercial_id"],
                            total_amount=data["total_amount"],
                            bill_to_pay=data["bill_to_pay"],
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
    def update_contract(session, contract_id, data):
        session.query(Contract).filter_by(id=contract_id).update(data)
        session.commit()

    def delete_contract(self, session, contract_id):
        events = session.query(Event).filter_by(contract_id=contract_id).first()

        if events or (isinstance(events, list) and (None,) not in events):
            self.main_controller.view.display_cannot_delete(model_type="contract",
                                                            model_linked="event")
            return False

        session.query(Contract).filter_by(id=contract_id).delete()
        session.commit()
        return True

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
