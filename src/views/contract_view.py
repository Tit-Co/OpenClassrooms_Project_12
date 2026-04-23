from __future__ import annotations

from typing import TYPE_CHECKING

from src.models.contract import Contract

if TYPE_CHECKING:
    from src.views.main_view import MainView


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
            print(f"  - {contract.id}. Contract between the client {client.name if client else '[unknown]'} "
                  f"and the commercial {commercial.name if commercial else '[unknown]'}")

    def display_contract(self, contract: type[Contract]) -> None:
        """
        Method to display a contract
        Args:
            contract (type[Contract]):
        """
        self.main_view.display_title(model_type="contract")

        print(f"Id : {contract.id}")
        print(f"Client name : {contract.client_name if contract.client_name else ''}")
        print(f"Client email : {contract.client_email if contract.client_email else ''}")
        print(f"Client phone : {contract.client_phone if contract.client_phone else ''}")
        print(f"Commercial name : {contract.commercial_name if contract.commercial_name else ''}")
        print(f"Total amount : {contract.total_amount} $")
        print(f"Bill to pay : {contract.bill_to_pay} $")
        print(f"Creation date : {contract.creation_date}")
        print(f"Contract signed : {'✅' if contract.status else '❌'}")

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
            answer = input(f"\n▶ Please select a {model_type} for the contract if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

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
                answer = input("\n▶ Please type the contract total amount if possible:\n▶▶ ").strip()
            else:
                answer = input("\n▶ Please type the amount left to pay if existing:\n▶▶ ").strip()

            if self.is_float(answer) or answer.isdigit() or answer == "":
                return float(answer) if answer else None

            print(f"Please enter a number or leave blank to continue.")

    @staticmethod
    def prompt_for_contract_boolean() -> bool:
        """
        Method that prompts the user to enter the boolean value for the contract status
        (signed or not)
        Returns:

        """
        while True:
            status = input("\n▶ Is the contract signed (y/n):\n▶▶ ")

            if status.lower() in ["y", "n"]:
                return status == "y"

            print(f"Please enter either 'y' or 'n'.")
