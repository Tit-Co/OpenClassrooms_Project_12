from __future__ import annotations

import sys
import click

from typing import TYPE_CHECKING, Any
from rich.console import Console
from rich.panel import Panel
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
    def display_client(client: type[Client]) -> Panel:
        """
        Method that displays the client
        Args:
            client (Client): Client object
        Returns:
            A Panel object
        """
        table = Table(show_header=False, border_style="black")
        table.add_row(f"[bold light_salmon3]Id[/bold light_salmon3] :  : {client.id}")
        table.add_row(f"[bold light_salmon3]name[/bold light_salmon3] : {client.name}")
        table.add_row(f"[bold light_salmon3]E-mail[/bold light_salmon3] : {client.email}")
        table.add_row(f"[bold light_salmon3]Phone[/bold light_salmon3] : {client.phone}")
        table.add_row(f"[bold light_salmon3]Company[/bold light_salmon3] : {client.company}")
        table.add_row(f"[bold light_salmon3]Creation date[/bold light_salmon3] : {client.creation_date}")
        table.add_row(f"[bold light_salmon3]Last update[/bold light_salmon3] : {client.last_update}")
        table.add_row(f"[bold light_salmon3]Commercial name[/bold light_salmon3] : {client.commercial_name or ''}\n")

        return Panel(table, border_style="bold cornflower_blue", expand=True)

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
        answer = click.prompt(f"\n▶ Please select a {model_type} for the client if possible:\n▶▶ ",
                                  type=int).strip()
        return answer

    def prompt_for_client_email(self) -> str:
        """
        Method that prompts the user to enter the client email
        Returns:
        The email
        """
        return self.main_view.prompt_for_email()
