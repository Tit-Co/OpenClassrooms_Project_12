from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from src.controllers.main_controller import MainController

from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Technician


class EventController:
    def __init__(self, main_controller: MainController) -> None:
        self.main_controller = main_controller

    def create_event_with_view(self, session: Session) -> None:
        """
        Method to create event with view
        Args:
            session (Session): session
        """
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

    def create_event(self, session: Session, data: dict) -> Event | None:
        """
        Method to create event
        Args:
            session (Session): session
            data (dict): data

        Returns:
        The event object
        """
        event = Event(name=data["name"],
                      contract_id=data["contract_id"],
                      start_date=data["start_date"],
                      end_date=data["end_date"],
                      technician_id=data["technician_id"],
                      location=data["location"],
                      attendees=data["attendees"],
                      notes=data["notes"])

        session.add(event)
        try:
            session.commit()
            return event

        except SQLAlchemyError:
            session.rollback()
            self.main_controller.view.display_database_error()
            return None

    def update_event_with_view(self, session: Session) -> None:
        """
        Method to update event with view
        Args:
            session (Session): session
        """
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
                self.main_controller.view.display_something_wrong("updating")

    def update_event(self, session: Session, event_id: int, data: dict) -> None:
        """
        Method to update event with view
        Args:
            session (Session): session
            event_id (int): event id
            data (dict): data
        """
        session.query(Event).filter_by(is_active=True, id=event_id).update(data)
        try:
            session.commit()

        except SQLAlchemyError:
            session.rollback()
            self.main_controller.view.display_database_error()

    def delete_event(self, session: Session, event_id: int) -> bool:
        """
        Method to delete event
        Args:
            session (Session): session
            event_id (int): event id

        Returns:
        A boolean indicating if the event was deleted successfully
        """
        session.query(Event).filter_by(is_active=True, id=event_id).update({"is_active": False})

        try:
            session.commit()
            return True

        except SQLAlchemyError:
            session.rollback()
            self.main_controller.view.display_database_error()
            return False

    @staticmethod
    def get_event(session: Session, model_id: int) -> Event:
        """
        Method to get event by its id
        Args:
            session (Session): session
            model_id (int): model id

        Returns:
        The event object
        """
        selection = (select(Event, Technician, Contract, Client)
                        .join(Event.technician, isouter=True)
                        .join(Event.contract, isouter=True)
                        .join(Client, Client.id == Contract.client_id)
                        .where(
                            Event.is_active == True,
                            Event.id == model_id
                        )
                    )
        result = session.execute(selection).first()
        event, technician, contract, client = result

        event.technician_name = technician.name if technician and technician.is_active else ""
        event.client_name = client.name if client and client.is_active else ""
        event.client_email = client.email if client and client.is_active else ""
        event.client_phone = client.phone if client and client.is_active else ""

        return event

    def filter_event(self, session: Session,
                     my_filter: str,
                     filter_value: str | int | float,
                     class_name: Event) -> list:
        """
        Method to filter event
        Args:
            session (Session): Session object
            my_filter (str): The filter.
            filter_value (str | int | float): The filter value.
            class_name (Event): The Event class name.

        Returns:

        """
        results = []

        if my_filter == "name":
            results = (session.query(class_name)
                       .filter(class_name.is_active == True, class_name.name.contains(filter_value)).all())

        elif my_filter == "location":
            results = (session.query(class_name)
                       .filter(class_name.is_active == True, class_name.location.contains(filter_value)).all())

        elif my_filter == "attendees-max":
            results = (session.query(class_name)
                       .filter(class_name.is_active == True, class_name.attendees < filter_value).all())

        elif my_filter == "prior-date":
            results = (
                session.query(class_name)
                .filter(
                    class_name.is_active == True,
                    class_name.start_date < filter_value
                )
                .all()
            )

        elif my_filter == "afterward-date":
            results = (
                session.query(class_name)
                .filter(
                    class_name.is_active == True,
                    class_name.start_date > filter_value
                )
                .all()
            )

        elif my_filter == "no-technician":
            results = session.query(class_name).filter_by(is_active=True, technician_id=None).all()

        elif my_filter == "technician-id":
            results = session.query(class_name).filter_by(is_active=True, technician_id=filter_value).all()

        elif my_filter == "technician-name":
            results = (
                session.query(class_name)
                .join(class_name.technician)
                .filter(
                    class_name.is_active == True,
                    Technician.name.contains(filter_value)
                ).all())

        results = [self.get_event(session=session, model_id=result.id) for result in results]
        return results
