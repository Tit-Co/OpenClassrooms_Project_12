from __future__ import annotations

import sys
import click

from datetime import datetime
from typing import TYPE_CHECKING
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models.event import Event

if TYPE_CHECKING:
    from src.views.main_view import MainView


console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200
)


class EventView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    def display_event(self, event: Event) -> Panel:
        """
        Method to display an event
        Args:
            event (type[Event]): The event to display
        Returns:
            A Panel containing the event
        """
        table = Table(show_header=False, border_style="black")
        table.add_row(f"[light_salmon3]Id[/light_salmon3] : {event.id}")
        table.add_row(f"[light_salmon3]Name[/light_salmon3] : {event.name}")
        table.add_row(f"[light_salmon3]Contract id[/light_salmon3] : {event.contract_id}")
        table.add_row(f"[light_salmon3]Client name[/light_salmon3] : {event.client_name if event.client_name else "[unknown]"}")
        table.add_row(f"[light_salmon3]Client phone[/light_salmon3] : {event.client_phone if event.client_phone else "[unknown]"}")
        table.add_row(f"[light_salmon3]Client e-mail[/light_salmon3] : {event.client_email if event.client_email else "[unknown]"}")
        table.add_row(f"[light_salmon3]Start date[/light_salmon3] : {event.start_date if event.start_date else ""}")
        table.add_row(f"[light_salmon3]End date[/light_salmon3] : {event.end_date if event.end_date else ""}")
        table.add_row(f"[light_salmon3]Technician name[/light_salmon3] : {event.technician_name if event.technician_name else "[unknown]"}")
        table.add_row(f"[light_salmon3]Location[/light_salmon3] : {event.location if event.location else ""}")
        table.add_row(f"[light_salmon3]Attendees[/light_salmon3] : {event.attendees if event.attendees else ""}")
        table.add_row(f"[light_salmon3]Notes[/light_salmon3] : {event.notes if event.notes else ""}\n")

        return Panel(table, border_style="bold chartreuse2", expand=True)

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
