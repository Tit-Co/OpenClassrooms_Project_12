from src.models.contract import Contract
from src.models.client import Client
from src.models.event import Event
from src.models.user import Technician


class EventController:
    def __init__(self, main_controller):
        self.main_controller = main_controller

    def create_event_with_view(self, session):
        contracts = self.main_controller.user_controller.get_models(session=session,
                                                                    model_type="contract")
        technicians = self.main_controller.user_controller.get_models(session=session,
                                                                      model_type="technician")

        (name,
         contract_id,
         start_date,
         end_date,
         technician_id,
         location,
         attendees,
         notes
         ) = self.main_controller.view.event_view.prompt_for_event(contracts=contracts,
                                                                   technicians=technicians)

        if not self.main_controller.user_controller.model_exists(session=session,
                                                                 model_type="event",
                                                                 value=name):
            data = {
                "name": name,
                "contract_id": contract_id,
                "start_date": start_date,
                "end_date": end_date,
                "technician_id": technician_id,
                "location": location,
                "attendees": attendees,
                "notes": notes
            }

            event = self.create_event(session=session, data=data)
            event = self.get_event(session=session, model_id=event.id)

            self.main_controller.view.display_action_successfully_done(action="created",
                                                                       model_type="event")

            self.main_controller.view.event_view.display_event(event=event)
        else:
            self.main_controller.view.display_model_already_exist(model_type="event")

    @staticmethod
    def create_event(session, data):
        event = Event(name=data["name"],
                      contract_id=data["contract_id"],
                      start_date=data["start_date"],
                      end_date=data["end_date"],
                      technician_id=data["technician_id"],
                      location=data["location"],
                      attendees=data["attendees"],
                      notes=data["notes"])

        session.add(event)
        session.commit()
        return event

    def update_event_with_view(self, session):
        events = self.main_controller.user_controller.get_models(session=session,
                                                                 model_type="event")
        contracts = self.main_controller.user_controller.get_models(session=session,
                                                                    model_type="contract")
        technicians = self.main_controller.user_controller.get_models(session=session,
                                                                      model_type="technician")

        self.main_controller.view.display_models(model_type="event", models=events)

        if events:
            event_id = self.main_controller.view.prompt_for_model_id(model_type="event",
                                                                     models=events)

            event = self.get_event(session=session, model_id=event_id)
            self.main_controller.view.event_view.display_event(event=event)

            self.main_controller.view.display_new_data_request(model_type="event",
                                                               model_id=event_id)

            (name,
             contract_id,
             start_date,
             end_date,
             technician_id,
             location,
             attendees,
             notes
             ) = self.main_controller.view.event_view.prompt_for_event(contracts=contracts,
                                                                       technicians=technicians)

            new_contract_data = {
                "name": name,
                "contract_id": contract_id,
                "start_date": start_date,
                "end_date": end_date,
                "technician_id": technician_id,
                "location": location,
                "attendees": attendees,
                "notes": notes
            }
            self.update_event(session=session, event_id=event_id, data=new_contract_data)

            event = self.get_event(session=session, model_id=event_id)

            if event or (isinstance(event, list) and (None,) not in event):
                self.main_controller.view.display_action_successfully_done(action="updated",
                                                                           model_type="event")

                self.main_controller.view.event_view.display_event(event=event)

            else:
                self.main_controller.view.display_something_wrong_while_updating()

    @staticmethod
    def update_event(session, event_id, data):
        session.query(Event).filter_by(id=event_id).update(data)
        session.commit()

    @staticmethod
    def delete_event(session, event_id):
        session.query(Event).filter_by(id=event_id).delete()
        session.commit()
        return True

    @staticmethod
    def get_event(session, model_id):
        event = session.query(Event).filter_by(id=model_id).first()
        technician = session.query(Technician).filter_by(id=event.technician_id).first()
        contract = session.query(Contract).filter_by(id=event.contract_id).first()
        client = session.query(Client).filter_by(id=contract.client_id).first()
        event.technician_name = technician.name if technician else ""
        event.client_name = client.name if client else ""
        event.client_phone = client.phone if client else ""
        event.client_email = client.email if client else ""

        return event
