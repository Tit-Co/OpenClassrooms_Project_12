from datetime import datetime

from src.models.client import Client
from src.models.contract import Contract
from src.models.user import Commercial



class ClientController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def create_client_with_view(self, session):
        commercials = self.main_controller.user_controller.get_models(session=session, model_type="commercial")

        (commercial_id,
         name,
         email,
         phone,
         company
         ) = self.main_controller.view.client_view.prompt_for_client(commercials=commercials)

        if not self.main_controller.model_exists(session=session,
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

            self.main_controller.view.client_view.display_client(client=client)

        self.main_controller.view.display_model_already_exist(model_type="client")

    @staticmethod
    def create_client(session, data):
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

    def update_client_with_view(self, session):
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
    def update_client(session, client_id, data):
        session.query(Client).filter_by(id=client_id).update(data)
        session.commit()

    def delete_client(self, session, client_id):
        client = session.query(Contract).filter_by(client_id=client_id).first()
        if client and (None,) not in client:
            self.main_controller.view.display_cannot_delete(model_type="client",
                                                            model_linked="contract")
            return

        session.query(Client).filter_by(id=client_id).delete()
        session.commit()

    @staticmethod
    def get_client(session, model_id):
        client = session.query(Client).filter_by(id=model_id).first()
        commercial = session.query(Commercial).filter_by(id=client.commercial_id).first()
        client.commercial_name = commercial.name if commercial else ""

        return client
