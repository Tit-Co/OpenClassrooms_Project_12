from typing import Any

from src.models.client import Client


class ClientView:
    def __init__(self, main_view):
        self.main_view = main_view

    def display_client(self, client: type[Client]) -> None:
        """
        Method that displays the client
        Args:
            client (Client): Client object
        """
        self.main_view.display_title(model_type="client")
        print(f"Id : {client.id}")
        print(f"name : {client.name}")
        print(f"E-mail : {client.email}")
        print(f"Phone : {client.phone}")
        print(f"Company : {client.company}")
        print(f"Creation date : {client.creation_date}")
        print(f"Last update : {client.last_update}")
        print(f"Commercial name : {client.commercial_name or ''}")

    def prompt_for_client(self, commercials: list) -> tuple[None, Any, None, Any, Any]:
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
            answer = input(f"\n▶ Please select a {model_type} for the client if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

    def prompt_for_client_email(self) -> str:
        """
        Method that prompts the user to enter the client email
        Returns:
        The email
        """
        return self.main_view.prompt_for_email(model_type=" client")
