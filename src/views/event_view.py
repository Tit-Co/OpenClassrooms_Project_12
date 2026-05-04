from __future__ import annotations

import sys
from datetime import datetime
from typing import TYPE_CHECKING

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.models.event import Event

if TYPE_CHECKING:
    from src.views.main_view import MainView


class EventView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    @property
    def console(self) -> Console:
        return self.main_view.console

    def display_events(self, models: list) -> None:
        """
        Method to display the list of clients
        Args:
            models (list): List of clients
        """
        events = models
        for event in events:
            self.console.print(Panel(f"  [spring_green3]- [bold]{event.id}.[/bold] {event.name}"
                                f"[/spring_green3]",
                                border_style="bold spring_green3",
                                expand=False))

    @staticmethod
    def display_event(event: Event) -> Panel:
        """
        Method to display an event
        Args:
            event (type[Event]): The event to display
        Returns:
            A Panel containing the event
        """
        table = Table(show_header=False, box=None)
        table.add_row(f"[spring_green3]Id[/spring_green3] : {event.id}")
        table.add_row(f"[spring_green3]Name[/spring_green3] : {event.name}")
        table.add_row(f"[spring_green3]Contract id[/spring_green3] : {event.contract_id}")
        table.add_row(f"[spring_green3]Client name[/spring_green3] : {event.client_name if event.client_name else "[unknown]"}")
        table.add_row(f"[spring_green3]Client phone[/spring_green3] : {event.client_phone if event.client_phone else "[unknown]"}")
        table.add_row(f"[spring_green3]Client e-mail[/spring_green3] : {event.client_email if event.client_email else "[unknown]"}")
        table.add_row(f"[spring_green3]Start date[/spring_green3] : {event.start_date if event.start_date else ""}")
        table.add_row(f"[spring_green3]End date[/spring_green3] : {event.end_date if event.end_date else ""}")
        table.add_row(f"[spring_green3]Technician name[/spring_green3] : {event.technician_name if event.technician_name else "[unknown]"}")
        table.add_row(f"[spring_green3]Location[/spring_green3] : {event.location if event.location else ""}")
        table.add_row(f"[spring_green3]Attendees[/spring_green3] : {event.attendees if event.attendees else ""}")
        table.add_row(f"[spring_green3]Notes[/spring_green3] : {event.notes if event.notes else ""}\n")

        return Panel(table, border_style="bold spring_green3", expand=False)

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
        contract_id = self.prompt_for_id(model_type="contract", models=contracts)

        self.main_view.display_models(model_type="technician", models=technicians)
        technician_id = self.prompt_for_id(model_type="technician", models=technicians)

        name = self.main_view.prompt_for_string(model_type="event", field="name")

        start_date = self.main_view.prompt_for_date(model_type="event", field="start date")

        end_date = self.main_view.prompt_for_date(model_type="event", field="end date")

        location = self.main_view.prompt_for_string_if_known(model_type="event", field="location")

        attendees = self.prompt_for_integer()

        notes = self.main_view.prompt_for_string_if_known(model_type="event", field="notes")

        return name, contract_id, start_date, end_date, technician_id, location, attendees, notes

    def prompt_for_id(self, model_type: str, models: list) -> int | None:
        """
        Method that prompts the user to enter the id for the model
        Args:
            model_type (str): The model type
            models (list): List of models

        Returns:
        The id of the model or None
        """
        while True:
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▶ Please select a {model_type} for the event if possible"
                                f"[/bold light_goldenrod2]\n"
                                f"[dark_turquoise]▶▶[/dark_turquoise] ",
                                default=1).strip()

            if not answer.isdigit():
                self.console.print("\n❗ [bold red]Please enter a number.\n[/bold red]")
                continue

            coll = (str(i + 1) for i in range(len(models)))

            if answer not in coll:
                self.console.print(f"\n❗ [bold red]Please choose between 1 and {len(models)}.\n[/bold red]")
                continue

            return int(answer)

    def prompt_for_integer(self) -> int | None:
        """
        Method that prompts the user to enter an integer
        Returns:
        The integer or None
        """
        while True:
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▶ Please enter the number of attendees if known"
                                f"[/bold light_goldenrod2]\n"
                                f"[dark_turquoise]▶▶[/dark_turquoise] ").strip()

            if not answer.isdigit():
                self.console.print("\n❗ [bold red]Please enter a number.\n[/bold red]")
                continue

            return int(answer)
