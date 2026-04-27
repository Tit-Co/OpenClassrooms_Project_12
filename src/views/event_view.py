from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import click

from src.models.event import Event

if TYPE_CHECKING:
    from src.views.main_view import MainView


class EventView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    def display_event(self, event: Event) -> None:
        """
        Method to display an event
        Args:
            event (type[Event]): The event to display
        """
        self.main_view.display_title(model_type="event")
        click.echo(f"Id : {event.id}")
        click.echo(f"Name : {event.name}")
        click.echo(f"Contract id : {event.contract_id}")
        click.echo(f"Client name : {event.client_name if event.client_name else "[unknown]"}")
        click.echo(f"Client phone : {event.client_phone if event.client_phone else "[unknown]"}")
        click.echo(f"Client e-mail : {event.client_email if event.client_email else "[unknown]"}")
        click.echo(f"Start date : {event.start_date if event.start_date else ""}")
        click.echo(f"End date : {event.end_date if event.end_date else ""}")
        click.echo(f"Technician name : {event.technician_name if event.technician_name else "[unknown]"}")
        click.echo(f"Location : {event.location if event.location else ""}")
        click.echo(f"Attendees : {event.attendees if event.attendees else ""}")
        click.echo(f"Notes : {event.notes if event.notes else ""}\n")

    def prompt_for_event(self, contracts: list, technicians: list) -> tuple[
        str, int, datetime | None, datetime | None, int | None, str | None, int | None, str | None]:
        """
        Method that prompts the user to enter the event data
        Args:
            contracts (list): List of contract
            technicians (list): List of technicians

        Returns:
        A tuple with the event data
        """
        self.main_view.display_models(model_type="contract", models=contracts)
        contract_id = self.prompt_for_id(model_type="contract")

        self.main_view.display_models(model_type="technician", models=technicians)
        technician_id = self.prompt_for_id(model_type="technician")

        name = self.main_view.prompt_for_string(model_type="event", field="name")

        start_date = self.main_view.prompt_for_date(model_type="event", field="start date")

        end_date = self.main_view.prompt_for_date(model_type="event", field="end date")

        location = self.main_view.prompt_for_string_if_known(model_type="event", field="location")

        attendees = self.prompt_for_integer()

        notes = self.main_view.prompt_for_string_if_known(model_type="event", field="notes")

        return name, contract_id, start_date, end_date, technician_id, location, attendees, notes

    @staticmethod
    def prompt_for_id(model_type: str) -> int | None:
        """
        Method that prompts the user to enter the id for the model
        Args:
            model_type (str): The model type

        Returns:
        The id of the model or None
        """
        answer = click.prompt(f"\n▶ Please select a {model_type} for the event if possible:\n▶▶ ",
                              type=int).strip()
        return answer

    @staticmethod
    def prompt_for_integer() -> int | None:
        """
        Method that prompts the user to enter an integer
        Returns:
        The integer or None
        """
        answer = click.prompt(f"\n▶ Please enter the number of attendees if known:\n▶▶ ", type=int).strip()

        return answer
