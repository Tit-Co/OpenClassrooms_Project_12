from __future__ import annotations

import sys
import click

from typing import TYPE_CHECKING, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.models.client import Client

if TYPE_CHECKING:
    from src.views.main_view import MainView


console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200
)


class ClientView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    @staticmethod
    def display_clients(models: list) -> None:
        """
        Method to display the list of clients
        Args:
            models (list): List of clients
        """
        clients = models
        for client in clients:
            console.print(Panel(f"  [deep_sky_blue1]- [bold]{client.id}.[/bold] {client.name}"
                                f"[/deep_sky_blue1]",
                                border_style="bold deep_sky_blue1",
                                expand=False))

    @staticmethod
    def display_client(client: type[Client]) -> Panel:
        """
        Method that displays the client
        Args:
            client (Client): Client object
        Returns:
            A Panel object
        """
        table = Table(show_header=False, box=None)
        table.add_row(f"[bold deep_sky_blue1]Id[/bold deep_sky_blue1] :  : {client.id}")
        table.add_row(f"[bold deep_sky_blue1]name[/bold deep_sky_blue1] : {client.name}")
        table.add_row(f"[bold deep_sky_blue1]E-mail[/bold deep_sky_blue1] : {client.email}")
        table.add_row(f"[bold deep_sky_blue1]Phone[/bold deep_sky_blue1] : {client.phone}")
        table.add_row(f"[bold deep_sky_blue1]Company[/bold deep_sky_blue1] : {client.company}")
        table.add_row(f"[bold deep_sky_blue1]Creation date[/bold deep_sky_blue1] : {client.creation_date}")
        table.add_row(f"[bold deep_sky_blue1]Last update[/bold deep_sky_blue1] : {client.last_update}")
        table.add_row(f"[bold deep_sky_blue1]Commercial name[/bold deep_sky_blue1] : {client.commercial_name or ''}\n")

        return Panel(table, border_style="bold deep_sky_blue1", expand=False)

    def prompt_for_client(self, commercials: list) -> tuple[int | None, Any, str, Any, Any]:
        """
        Method that prompts the user to enter the client data and choose a commercial
        Args:
            commercials (list): List of commercials

        Returns:

        """
        self.main_view.display_models("commercial", commercials)
        client_id = self.prompt_for_id(model_type="commercial")

        name = self.main_view.prompt_for_string(model_type="client", field="name")

        email = self.prompt_for_client_email()

        phone = self.main_view.prompt_for_string_if_known(model_type="client", field="phone")

        company =  self.main_view.prompt_for_string_if_known(model_type="client", field="company")

        return client_id, name, email, phone, company

    @staticmethod
    def prompt_for_id(model_type: str) -> int | None:
        """
        Method that prompts the user to enter the client ID
        Args:
            model_type (str): Type of model

        Returns:
        The id or None
        """
        while True:
            answer = Prompt.ask(f"\n▶ Please select a {model_type} for the client if possible\n"
                                f"▶▶ ").strip()

            if not answer.isdigit():
                console.print("\n❗ [bold red]Please enter a number.\n[/bold red]")
                continue

            return None if answer == "" or int(answer) == 0 else int(answer)

    def prompt_for_client_email(self) -> str:
        """
        Method that prompts the user to enter the client email
        Returns:
        The email
        """
        return self.main_view.prompt_for_email()
