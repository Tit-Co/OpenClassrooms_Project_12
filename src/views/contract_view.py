from __future__ import annotations
from typing import TYPE_CHECKING

import sys
import click

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.models.contract import Contract

if TYPE_CHECKING:
    from src.views.main_view import MainView


console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200
)


class ContractView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    @staticmethod
    def is_float(s: str) -> bool:
        """
        Method that checks if the input is a float
        Args:
            s (str): The input string

        Returns:
        A boolean that indicates if the input is a float or not
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def display_contracts(models: dict) -> None:
        """
        Method to display the list of contracts
        Args:
            models ():
        """
        clients = models.get("clients")
        commercials = models.get("commercials")
        contracts = models.get("contracts")
        for contract in contracts:
            client_id = contract.client_id
            commercial_id = contract.commercial_id
            client = next((c for c in clients if c.id == client_id), None)
            commercial = next((c for c in commercials if c.id == commercial_id), None)

            console.print(Panel(f"  - [bold red]{contract.id}.[/bold red] Contract between "
                                f"the client {client.name if client else '[unknown]'} "
                                f"and the commercial {commercial.name if commercial else '[unknown]'}",
                                border_style="dark_red", expand=True))

    @staticmethod
    def display_contract(contract: type[Contract]) -> Panel:
        """
        Method to display a contract
        Args:
            contract (type[Contract]):
        """
        table = Table(show_header=False, border_style="black")
        table.add_row(f"[bold light_salmon3]Id[/bold light_salmon3] : {contract.id}")
        table.add_row(f"[bold light_salmon3]Client name[/bold light_salmon3] : {contract.client_name \
            if contract.client_name else ''}")
        table.add_row(f"[bold light_salmon3]Client email[/bold light_salmon3] : {contract.client_email \
            if contract.client_email else ''}")
        table.add_row(f"[bold light_salmon3]Client phone[/bold light_salmon3] : {contract.client_phone \
            if contract.client_phone else ''}")
        table.add_row(f"[bold light_salmon3]Commercial name[/bold light_salmon3] : {contract.commercial_name \
            if contract.commercial_name else ''}")
        table.add_row(f"[bold light_salmon3]Total amount[/bold light_salmon3] : {contract.total_amount} $")
        table.add_row(f"[bold light_salmon3]Bill to pay[/bold light_salmon3] : {contract.bill_to_pay} $")
        table.add_row(f"[bold light_salmon3]Creation date[/bold light_salmon3] : {contract.creation_date}")
        table.add_row(f"[bold light_salmon3]Contract signed[/bold light_salmon3] : {'✅' if contract.status else '❌'}\n")

        return Panel(table, border_style="bold dark_red", expand=True)

    def prompt_for_contract(self, clients: list, commercials: list) -> tuple[
        int | None, int | None, float | None, float | None, bool]:
        """
        Method that prompts the user to enter the contract data
        Args:
            clients (list): The clients list
            commercials (list): The commercials list

        Returns:
        A tuple with the contract data
        """
        self.main_view.display_models(model_type="client", models=clients)
        client_id = self.prompt_for_id(model_type="client")

        self.main_view.display_models(model_type="commercial", models=commercials)
        commercial_id = self.prompt_for_id(model_type="commercial")

        total_amount = self.prompt_for_contract_float_number(amount_type="total_amount")

        bill_to_pay = self.prompt_for_contract_float_number(amount_type="bill_to_pay")

        status = self.prompt_for_contract_boolean()

        return client_id, commercial_id, total_amount, bill_to_pay, status

    @staticmethod
    def prompt_for_id(model_type: str) -> int | None:
        """
        Method that prompts the user to enter the id of a model or leave it blank
        Args:
            model_type (str): The type of the model

        Returns:
        The id of the model
        """
        choice = click.prompt(f"\n▶ Please select a {model_type} for the contract if possible:\n▶▶ ",
                              type=int,
                              default=0)

        return None if choice == 0 else choice

    @staticmethod
    def prompt_for_contract_float_number(amount_type: str) -> float | None:
        """
        Method that prompts the user to enter the float number or leave it blank
        Args:
            amount_type (str): The type of the amount

        Returns:
        The float number or None
        """
        while True:
            if amount_type == "total_amount":
                answer = click.prompt("\n▶ Please type the contract total amount if possible:\n▶▶ ",
                                      type=float)
            else:
                answer = click.prompt("\n▶ Please type the amount left to pay if existing:\n▶▶ ",
                                      type=float)


            return answer

    @staticmethod
    def prompt_for_contract_boolean() -> bool:
        """
        Method that prompts the user to enter the boolean value for the contract status
        (signed or not)
        Returns:

        """
        return click.prompt("\n▶ Is the contract signed :\n▶▶ ", type=bool, default=False)
