import re
from datetime import datetime

from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Commercial, Manager, Technician
from src.views.client_view import ClientView
from src.views.contract_view import ContractView
from src.views.event_view import EventView


class MainView:
    def __init__(self):
        self.contract_view = ContractView(self)
        self.client_view = ClientView(self)
        self.event_view = EventView(self)

    @staticmethod
    def display_main_menu() -> None:
        """
        Method to display the main menu.
        """
        print("\nWELCOME TO EPIC EVENTS !\n")
        print("▶ MAIN MENU ◀")
        print("▷▷ 1. Log in")
        print("▷▷ 2. Quit the app\n")

    @staticmethod
    def display_goodbye() -> None:
        """
        Method to display the goodbye message.
        """
        print("\n👋  Goodbye ! 👋\n")

    @staticmethod
    def display_logout() -> None:
        """
        Method to display the logout message.
        """
        print("\nYou are successfully logged out.\n")

    @staticmethod
    def display_submenu(model_type) -> None:
        """
        Method to display the submenu.
        Args:
            model_type ():
        """
        print(f"\n▶ {model_type.upper()} MENU ◀\n")
        print("▷▷ 1. Display")
        print("▷▷ 2. Create")
        print("▷▷ 3. Update")
        print("▷▷ 4. Delete")
        print("▷▷ 5. Filter")
        print("▷▷ 6. Go back")

    @staticmethod
    def display_permission_denied(action: str, model_type: str) -> None:
        """
        Method to display the permission denied message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        print(f"You don't have permission to {action} a {model_type}.")

    @staticmethod
    def display_action_introduction(action: str, model_type: str) -> None:
        """
        Method to display the introduction message from an action.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        print(f"You are going to {action} a {model_type}.")

    @staticmethod
    def display_login_submenu() -> None:
        """
        Method to display the submenu after login.
        """
        print("\n▶ LOG IN ◀\n")
        print("▷▷ You are going to enter the followings details :")
        print(" • your e-mail address")
        print(" • your password\n")

    @staticmethod
    def display_successfully_logged_in(name: str) -> None:
        """
        Method to display the successfully logged in message.
        Args:
            name (str): The name of the user.
        """
        print(f"\n{name.capitalize()}, you are successfully logged in.\n")

    @staticmethod
    def display_action_successfully_done(action: str, model_type: str) -> None:
        """
        Method to display the successfully done message.
        Args:
            action ():
            model_type ():
        """
        print(f"\nThe {model_type} has been successfully {action}.\n")

    @staticmethod
    def display_wrong_password() -> None:
        """
        Method to display the wrong password message.
        """
        print("Invalid password.")

    @staticmethod
    def display_collaborator_does_not_exist() -> None:
        """
        Method to display the message when a collaborator does not exist.
        """
        print("This collaborator does not exist.")

    @staticmethod
    def display_collaborator_menu() -> None:
        """
        Method to display the collaborator menu when successfully logged in.
        """
        print(f"\n▶ EPIC EVENTS - COLLABORATOR MENU ◀\n")
        print("▷▷ 1. Collaborator")
        print("▷▷ 2. Contract")
        print("▷▷ 3. Client")
        print("▷▷ 4. Event")
        print("▷▷ 5. Log out\n")

    @staticmethod
    def display_collaborator_submenu() -> None:
        """
        Method to display the collaborator submenu.
        """
        print(f"\n▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀\n")
        print("▷▷ 1. Manager")
        print("▷▷ 2. Commercial")
        print("▷▷ 3. Technician")
        print("▷▷ 4. Go back\n")

    def display_models(self, model_type: str, models: list) -> None:
        """
        Method to display the models list
        Args:
            model_type (str): The model type.
            models (list): The models list.
        """
        if (None,) in models or not models:
            print(f"\n • {model_type}s - No {model_type} to display.\n")
        else:
            print(f"\n • {model_type}s - Here is the list : \n")

            actions = {
                "contract": self.contract_view.display_contracts,
                "client": self.display_clients_events,
                "event": self.display_clients_events,
                "manager": self.display_collaborators,
                "commercial": self.display_collaborators,
                "technician": self.display_collaborators,
            }

            action = actions.get(model_type)
            action(models)

    @staticmethod
    def display_clients_events(models: list) -> None:
        """
        Method to display the clients events.
        Args:
            models (list): The models list.
        """
        for model in models:
            print(f"  - {model.id}. {model.name}")

    @staticmethod
    def display_collaborators(models: list) -> None:
        """
        Method to display the collaborators list.
        Args:
            models ():
        """
        for model in models:
            print(f"  - {model.id}. {model.name.capitalize()}")

    def display_collaborator(self, collaborator: type[Commercial] | type[Manager] | type[Technician],
                             role: str) -> None:
        """
        Method to display the collaborator.
        Args:
            collaborator (type[Commercial] | type[Manager] | type[Technician]): The collaborator.
            role (str): The role of the collaborator.
        """
        self.display_title("Collaborator")
        print(f"{role.capitalize()} id : {collaborator.id}")
        print(f"Employee number : {collaborator.employee_number}")
        print(f"Name : {collaborator.name}")
        print(f"Email : {collaborator.email}")
        print(f"Role: {role}")

    @staticmethod
    def display_title(model_type: str) -> None:
        """
        Method to display a title for a given model.
        Args:
            model_type ():
        """
        print(f"\nHere is the {model_type} : \n")

    def display_model(self, model_type: str,
                      model: type[Client] | type[Event] | type[Contract]) -> None:
        """
        Method to display a model for a given type
        Args:
            model_type (str): The model type.
            model (type[Client] | type[Event] | type[Contract]): The model.
        """
        self.display_title(model_type)
        actions = {
            "contract": self.contract_view.display_contract,
            "client": self.client_view.display_client,
            "event": self.event_view.display_event
        }

        action = actions.get(model_type)
        action(model)

    @staticmethod
    def display_new_data_request(model_type: str, model_id: int) -> None:
        """
        Method to display a title for the new data request action for a given model type and model id.
        Args:
            model_type ():
            model_id ():
        """
        print(f"\n▶ Please enter the new data for the {model_type} n°{model_id}.")

    @staticmethod
    def display_model_already_exist(model_type: str) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            model_type ():
        """
        print(f"\n❌ This {model_type} already exists.\n")

    @staticmethod
    def display_something_wrong_while_updating() -> None:
        """
        Method to display a message when something goes wrong while updating
        """
        print("\n❌ Something went wrong while updating.\n")

    @staticmethod
    def display_cannot_delete(model_type, model_linked) -> None:
        """
        Method to display when deletion is not possible
        Args:
            model_type (str): The model type.
            model_linked (str): The model type linked to the model
        """
        print(f"\n❌ Cannot delete {model_type} : {model_linked}(s) linked.\n")

    @staticmethod
    def display_roles(roles: dict) -> None:
        """
        Method to display the roles list.
        Args:
            roles ():
        """
        print("\nAll roles:")
        for role_id, role_name in roles.items():
            print(f"  - {role_id}. {role_name.upper()}")

    @staticmethod
    def prompt_for_menu(nb) -> int | None:
        """
        Method to prompt the user to choose the action in the menu
        Args:
            nb (int): The number of choice.

        Returns:
        The choice
        """
        while True:
            answer = input("\n▶ What do you want to do ? \n▶▶ ")

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            coll = (str(i+1) for i in range(nb))
            if answer not in coll:
                print(f"Please choose between 1 and {nb}.")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_model_id_with_action(action: str, model_type: str, models: dict) -> int | None:
        """
        Method
        Args:
            action (str): The action to be performed.
            model_type (str): The model type
            models (list): The models list.

        Returns:
        The choice
        """
        while True:
            the_models = models
            if model_type == "contract":
                the_models = models.get("contracts")

            coll = [model.id for model in the_models]

            answer = input(f"\n▶ Which {model_type} do you want to {action} ? \n▶▶ ")

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            if int(answer) not in coll:
                print(f"Please choose a number from id {the_models[0].id} to id {the_models[-1].id}.")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_model_id(model_type: str, models: list) -> int | None:
        """
        Method to prompt the user to choose an id in the models list.
        Args:
            model_type (str): The model type.
            models (list): The models list.

        Returns:
        The choice or None
        """
        while True:
            coll = [model.id for model in models]

            answer = input(f"\n▷▷ Please choose a {model_type} :\n▶▶ ").strip()

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            if int(answer) not in coll:
                print(f"Please choose a number from id {models[0].id} to id {models[-1].id}.")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_continuing() -> str:
        """
        Method to prompt the user if he wants to continue.
        Returns:
        The answer (y/n)
        """
        while True:
            input_key = input("▷▷ Type 'q' to go back or anything else to continue : \n▶▶ ")
            return input_key.lower()

    @staticmethod
    def prompt_for_email(model_type: str) -> str | None:
        """
        Method to prompt the user the e-mail address.
        Args:
            model_type (str): The model type.

        Returns:
        The e-mail address or None
        """
        while True:
            email = input(f"\n▷▷ Enter the {model_type} e-mail address : \n▶▶ ")

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                print("Invalid e-mail address.")
                continue

            return email

    @staticmethod
    def prompt_for_password() -> str | None:
        """
        Method to prompt the user the password.
        Returns:
        The password or None
        """
        return input("\n▷▷ Enter the password : \n▶▶ ")

    @staticmethod
    def prompt_for_confirmation(action: str, model_type: str) -> bool:
        """
        Method to prompt the user to confirm the action.
        Args:
            action (str): The action to be performed.
            model_type (str): The model type.

        Returns:
        The confirmation answer (y/n)
        """
        while True:
            answer = input(f"\n▷▷ Are you sure you want to {action} this {model_type} (y/n) ?\n▶▶ ")

            if answer.lower() in ["y", "n"]:
                return True if answer.lower() == "y" else False

            print(f"Please enter either 'y' or 'n'.")

    @staticmethod
    def prompt_for_string(model_type: str, field: str) -> str:
        """
        Method to prompt the user to enter a string
        Args:
            model_type (str): The model type.
            field (str): The field to be entered.

        Returns:
        The string
        """
        while True:
            return input(f"\n▷▷ Please type the {model_type} {field}:\n▶▶ ")

    @staticmethod
    def prompt_for_string_if_known(model_type: str, field: str) -> str | None:
        """
        Method to prompt the user to enter a string or leave it blank
        Args:
            model_type (str): The model type.
            field (str): The field to be entered.

        Returns:
        The string or None
        """
        while True:
            return input(f"\n▷▷ Please type the {model_type} {field} or leave blank to continue:\n▶▶ ")

    @staticmethod
    def prompt_for_date(model_type: str, field: str) -> datetime | None:
        """
        Method to prompt the user to enter a date
        Args:
            model_type (str): The model type.
            field (str): The date field to be entered.

        Returns:
        A datetime or None
        """
        while True:
            answer = input(f"\n▷▷ Please enter the {model_type} {field} (dd/mm/yy hh:mm) "
                           f"or leave blank to continue:\n▶▶ ")
            if answer:

                answer += ':00'

                try:
                    return datetime.strptime(answer, '%d/%m/%y %H:%M:%S')

                except ValueError:
                    print("Please enter a valid date.")
            else:
                return None

    def prompt_for_collaborator(self, role) -> tuple[str, str, str]:
        """
        Method to prompt the user to enter the collaborator data
        Args:
            role (str): The role of the collaborator.

        Returns:
        A tuple with the e-mail, the password and the name of the collaborator.
        """
        email = self.prompt_for_email(role)

        password = self.prompt_for_password()

        name = self.prompt_for_string(model_type=role, field="name")

        return email, password, name

    def prompt_for_collaborator_role(self, roles: dict) -> tuple[int, str]:
        """
        Method to prompt the user to enter the collaborator role
        Args:
            roles (list): The roles available for the collaborator.

        Returns:
        A tuple with the role id and the role of the collaborator.
        """
        while True:
            self.display_roles(roles)

            role = input(f"\n▷▷ Which new role do you want to assign ? (1,2,3)\n▶▶ ")

            if role.isdigit() and int(role) in [1,2,3]:
                return int(role), roles[int(role)]

            print("Please enter an integer between 1 and 3.")
