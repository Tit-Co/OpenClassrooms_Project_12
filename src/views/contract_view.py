from __future__ import annotations
from typing import TYPE_CHECKING

import sys
import click

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
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
    def is_bool(s: str) -> bool | None:
        if str(s).lower() == "true" or (s.isdigit() and int(s) == 1):
            return True
        elif str(s).lower() == "false" or (s.isdigit() and int(s) == 0):
            return False
        else:
            return None

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
        table = Table(show_header=False, box=None)
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

        return Panel(table, border_style="bold bright_red", expand=True)

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
        while True:
            choice = Prompt.ask(f"\n[bold light_goldenrod2]▶ Please select a {model_type} for the contract if possible"
                                f"[/bold light_goldenrod2]\n"
                                f"[dark_turquoise]▶▶[/dark_turquoise] ")

            if not choice.isdigit():
                console.print("\n❗ [bold red]Please enter a number.\n[/bold red]")
                continue

            return None if choice == "" or int(choice) == 0 else int(choice)

    def prompt_for_contract_float_number(self, amount_type: str) -> float | None:
        """
        Method that prompts the user to enter the float number or leave it blank
        Args:
            amount_type (str): The type of the amount

        Returns:
        The float number or None
        """
        while True:
            if amount_type == "total_amount":
                answer = Prompt.ask("\n[bold light_goldenrod2]▶ Please type the contract total amount if possible"
                                    "[bold light_goldenrod2]\n"
                                    "[dark_turquoise]▶▶[/dark_turquoise] ")
            else:
                answer = Prompt.ask("\n[bold light_goldenrod2]▶ Please type the amount left to pay if existing"
                                    "[/bold light_goldenrod2]\n"
                                    "[dark_turquoise]▶▶[/dark_turquoise] ")

            if not self.is_float(answer):
                console.print("\n❗ [bold red]Please enter a number.\n[/bold red]")
                continue

            return float(answer)

    def prompt_for_contract_boolean(self) -> bool | None:
        """
        Method that prompts the user to enter the boolean value for the contract status
        (signed or not)
        Returns:

        """
        while True:
            answer = Prompt.ask("\n[bold light_goldenrod2]▶ Is the contract signed [/bold light_goldenrod2]\n"
                                "[dark_turquoise]▶▶[/dark_turquoise] ",
                                default="False")

            if not self.is_bool(answer):
                console.print("\n❗ [bold red]Please enter a boolean (true/false | 1/0).\n[/bold red]")
                continue

            return bool(answer)
