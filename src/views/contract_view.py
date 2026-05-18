from __future__ import annotations

from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.controllers.helper_controller import is_bool, is_float
from src.models.contract import Contract

if TYPE_CHECKING:
    from src.views.main_view import MainView


class ContractView:
    def __init__(self, main_view: MainView):
        self.main_view = main_view

    @property
    def console(self) -> Console:
        return self.main_view.console

    def display_contracts(self, models: dict) -> None:
        """
        Method to display the list of contracts
        Args:
            models (dict): A dictionary that contains all contracts, clients and commercials
        """
        clients = models.get("clients")
        commercials = models.get("commercials")
        contracts = models.get("contracts")

        for contract in contracts:
            client_id = contract.client_id
            commercial_id = contract.commercial_id

            client = next((c for c in clients if c.id == client_id), None)
            client_name = client.name if client and client.name else "(unknown)"

            commercial = next((c for c in commercials if c.id == commercial_id), None)
            commercial_name = commercial.name if commercial and commercial.name else "(unknown)"

            self.console.print(Panel(renderable=f"  - {contract.id}. Contract between the client {client_name} "
                                                f"and the commercial {commercial_name}",
                                     border_style="bold bright_red",
                                     style="bright_red",
                                     expand=False))

    @staticmethod
    def display_contract(contract: type[Contract]) -> Panel:
        """
        Method to display a contract
        Args:
            contract (type[Contract]):
        """
        table = Table(show_header=False, box=None)
        table.add_row(f"[bright_red]Id[/bright_red] : {contract.id}")
        table.add_row(f"[bright_red]Client name[/bright_red] : "
                      f"{contract.client_name if contract.client_name else ''}")
        table.add_row(f"[bright_red]Client email[/bright_red] : "
                      f"{contract.client_email if contract.client_email else ''}")
        table.add_row(f"[bright_red]Client phone[/bright_red] : "
                      f"{contract.client_phone if contract.client_phone else ''}")
        table.add_row(f"[bright_red]Commercial name[/bright_red] : "
                      f"{contract.commercial_name if contract.commercial_name else ''}")
        table.add_row(f"[bright_red]Total amount[/bright_red] : ${contract.total_amount}")
        table.add_row(f"[bright_red]Bill to pay[/bright_red] : ${contract.bill_to_pay}")
        table.add_row(f"[bright_red]Creation date[/bright_red] : {contract.creation_date}")
        table.add_row(f"[bright_red]Contract signed[/bright_red] : {'✅' if contract.status else '❌'}\n")

        return Panel(table, border_style="bold bright_red", expand=False)

    def prompt_for_contract(self, clients: list, commercials: list) \
            -> tuple[int | None, int | None, float | None, float | None, bool | None]:
        """
        Method that prompts the user to enter the contract data
        Args:
            clients (list): The clients list
            commercials (list): The commercials list

        Returns:
        A tuple with the contract data
        """

        self.main_view.display_models(model_type="client", models=clients)

        client_id = self.prompt_for_id(model_type="client", models=clients)

        self.main_view.display_models(model_type="commercial", models=commercials)

        commercial_id = self.prompt_for_id(model_type="commercial", models=commercials)

        total_amount = self.prompt_for_contract_float_number(amount_type="total_amount")

        bill_to_pay = self.prompt_for_contract_float_number(amount_type="bill_to_pay")

        status = self.prompt_for_contract_boolean()

        return client_id, commercial_id, total_amount, bill_to_pay, status

    def prompt_for_id(self, model_type: str, models: list) -> int | None:
        """
        Method that prompts the user to enter the id of a model or leave it blank
        Args:
            model_type (str): The type of the model
            models (list): The objects list ( clients or commercials)

        Returns:
        The id of the model or None
        """
        while True:
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▶ Please select a {model_type} for the contract if possible"
                                f"[/bold light_goldenrod2]\n"
                                f"▶▶ ")

            if not answer.isdigit() and answer != "":
                self.console.print("\n[bold red3]❗ Please enter a number or leave blank.\n[/bold red3]")
                continue

            coll = [i.id for i in models]

            if answer != "" and answer.isdigit() and int(answer) != 0 and int(answer) not in coll:
                self.console.print(f"\n[bold red3]❗ Please choose an id "
                                   f"between {models[0].id} and {models[-1].id}."
                                   f"\n[/bold red3]")
                continue

            return None if (answer == "" or int(answer) == 0) else int(answer)

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
                                    "▶▶ ")
            else:
                answer = Prompt.ask("\n[bold light_goldenrod2]▶ Please type the amount left to pay if existing"
                                    "[/bold light_goldenrod2]\n"
                                    "▶▶ ")

            if not is_float(answer):
                self.console.print("\n[bold red3]❗ Please enter a number.\n[/bold red3]")
                continue

            return float(answer)

    def prompt_for_contract_boolean(self) -> bool | None:
        """
        Method that prompts the user to enter the boolean value for the contract status
        (signed or not)
        Returns:

        """
        while True:
            answer = Prompt.ask("\n[bold light_goldenrod2]▶ Is the contract signed "
                                "(true/false | 1/0) ?[/bold light_goldenrod2]\n"
                                "▶▶ ", default="false")

            if not is_bool(answer.lower().strip()):
                self.console.print("\n[bold red3]❗ Please enter a boolean (true/false | 1/0).\n[/bold red3]")
                continue

            return bool(answer)
