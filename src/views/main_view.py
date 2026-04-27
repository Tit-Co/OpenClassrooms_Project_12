import click
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
        click.echo("\nWELCOME TO EPIC EVENTS !\n")
        click.echo("▶ MAIN MENU ◀")
        click.echo("▷▷ 1. Log in")
        click.echo("▷▷ 2. Quit the app\n")

    @staticmethod
    def display_goodbye() -> None:
        """
        Method to display the goodbye message.
        """
        click.echo("\n👋  Goodbye ! 👋\n")

    @staticmethod
    def display_logout() -> None:
        """
        Method to display the logout message.
        """
        click.echo("\n✅ You are successfully logged out.\n")

    @staticmethod
    def display_submenu(model_type) -> None:
        """
        Method to display the submenu.
        Args:
            model_type ():
        """
        click.echo(f"\n▶ {model_type.upper()} MENU ◀\n")
        click.echo("▷▷ 1. Display")
        click.echo("▷▷ 2. Create")
        click.echo("▷▷ 3. Update")
        click.echo("▷▷ 4. Delete")
        click.echo("▷▷ 5. Filter")
        click.echo("▷▷ 6. Go back")

    @staticmethod
    def display_permission_denied(action: str, model_type: str) -> None:
        """
        Method to display the permission denied message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        click.echo(f"❌ You don't have the permission to {action} a {model_type}.")

    @staticmethod
    def display_action_introduction(action: str, model_type: str) -> None:
        """
        Method to display the introduction message from an action.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        click.echo(f"\nYou are going to {action} a {model_type}.\n")

    @staticmethod
    def display_login_submenu() -> None:
        """
        Method to display the submenu after login.
        """
        click.echo("\n▶ LOG IN ◀\n")
        click.echo("▷▷ You are going to enter the followings details :")
        click.echo(" • your e-mail address")
        click.echo(" • your password\n")

    @staticmethod
    def display_successfully_logged_in(name: str) -> None:
        """
        Method to display the successfully logged in message.
        Args:
            name (str): The name of the user.
        """
        click.echo(f"\n✅ {name.capitalize()}, you are successfully logged in.\n")

    @staticmethod
    def display_action_successfully_done(action: str, model_type: str) -> None:
        """
        Method to display the successfully done message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        click.echo(f"\n✅ The {model_type} has been successfully {action}.\n")

    @staticmethod
    def display_action_fails(action: str, model_type: str) -> None:
        """
        Method to display the failure message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        click.echo(f"\n❌ The {model_type} has not been {action}.\n")

    @staticmethod
    def display_not_connected() -> None:
        """
        Method to display when the user is not logged in.
        """
        click.echo("❗ You need to log in first.")

    @staticmethod
    def display_wrong_password() -> None:
        """
        Method to display the wrong password message.
        """
        click.echo("❗ Invalid password.")

    @staticmethod
    def display_collaborator_not_exists() -> None:
        """
        Method to display the message when a collaborator does not exist.
        """
        click.echo("❗ This collaborator does not exist.")

    @staticmethod
    def display_collaborator_menu() -> None:
        """
        Method to display the collaborator menu when successfully logged in.
        """
        click.echo(f"\n▶ EPIC EVENTS - COLLABORATOR MENU ◀\n")
        click.echo("▷▷ 1. Collaborator")
        click.echo("▷▷ 2. Contract")
        click.echo("▷▷ 3. Client")
        click.echo("▷▷ 4. Event")
        click.echo("▷▷ 5. Log out\n")

    @staticmethod
    def display_collaborator_submenu() -> None:
        """
        Method to display the collaborator submenu.
        """
        click.echo(f"\n▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀\n")
        click.echo("▷▷ 1. Manager")
        click.echo("▷▷ 2. Commercial")
        click.echo("▷▷ 3. Technician")
        click.echo("▷▷ 4. Go back\n")

    def display_models(self, model_type: str, models: list) -> None:
        """
        Method to display the models list
        Args:
            model_type (str): The model type.
            models (list): The models list.
        """
        if (None,) in models or not models:
            click.echo(f"\n • {model_type}s - No {model_type} to display.\n")
        else:
            click.echo(f"\n • {model_type}s - Here is the list : \n")

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
            click.echo(f"  - {model.id}. {model.name}")

    @staticmethod
    def display_collaborators(models: list) -> None:
        """
        Method to display the collaborators list.
        Args:
            models (list): The models list.
        """
        for model in models:
            click.echo(f"  - {model.id}. {model.name.capitalize()}")

    def display_collaborator(self, collaborator: type[Commercial] | type[Manager] | type[Technician],
                             role: str) -> None:
        """
        Method to display the collaborator.
        Args:
            collaborator (type[Commercial] | type[Manager] | type[Technician]): The collaborator.
            role (str): The role of the collaborator.
        """
        self.display_title("Collaborator")
        click.echo(f"{role.capitalize()} id : {collaborator.id}")
        click.echo(f"Employee number : {collaborator.employee_number}")
        click.echo(f"Name : {collaborator.name}")
        click.echo(f"Email : {collaborator.email}")
        click.echo(f"Role: {role}\n")

    @staticmethod
    def display_title(model_type: str) -> None:
        """
        Method to display a title for a given model.
        Args:
            model_type (str): The model type.
        """
        click.echo(f"\nHere is the {model_type} : \n")

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
            model_type (str): The model type.
            model_id (int): The model id.
        """
        click.echo(f"\n▶ Please enter the new data for the {model_type} n°{model_id}.")

    @staticmethod
    def display_model_already_exist(model_type: str) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            model_type (str): The model type.
        """
        click.echo(f"\n❌ This {model_type} already exists.\n")

    @staticmethod
    def display_collaborator_already_exists(collaborator: type[Commercial | Manager | Technician]) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            collaborator (type[Commercial | Manager | Technician]): The collaborator
        """
        click.echo(f"\n❌ The collaborator {collaborator.email} already exists.\n")

    @staticmethod
    def display_collaborator_already_exists_but_inactive(collaborator: \
            type[Commercial | Manager | Technician]) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            collaborator (type[Commercial] | type[Manager] | type[Technician]): The collaborator
        """
        click.echo(f"\n❗ A collaborator inactive with this email [{collaborator.email}] already exists.\n")

    @staticmethod
    def display_something_wrong(action: str) -> None:
        """
        Method to display a message when something goes wrong during the givent action.
        """
        click.echo(f"\n❌ Something went wrong while {action}.\n")

    @staticmethod
    def display_something_wrong_while_creating() -> None:
        """
        Method to display a message when something goes wrong while creating
        """
        click.echo("\n❌ Something went wrong while creating.\n")
        
    @staticmethod
    def display_something_wrong_while_updating() -> None:
        """
        Method to display a message when something goes wrong while updating
        """
        click.echo("\n❌ Something went wrong while updating.\n")

    @staticmethod
    def display_something_wrong_while_deleting() -> None:
        """
        Method to display a message when something goes wrong while deleting
        """
        click.echo("\n❌ Something went wrong while deleting.\n")

    @staticmethod
    def display_action_impossible(action: str) -> None:
        """
        Method to display a message when the action is not possible.
        """
        click.echo(f"\n❌ No models to {action}.\n")

    @staticmethod
    def display_cannot_delete_admin_manager_or_yourself() -> None:
        """
        Method to display a message when a user wants to delete the admin manager or its own profile
        """
        click.echo("\n❌ You can not delete the admin manager or your own account.\n")

    @staticmethod
    def display_cannot_delete(model_type, model_linked) -> None:
        """
        Method to display when deletion is not possible
        Args:
            model_type (str): The model type.
            model_linked (str): The model type linked to the model
        """
        click.echo(f"\n❌ Cannot delete {model_type} : {model_linked}(s) linked.\n")

    @staticmethod
    def display_wrong_collaborator_role():
        """
        Method to display a message when the user enters a wrong collaborator role.
        """
        click.echo("❌ You did not enter a valid role as below : [manager/commercial/technician].")

    @staticmethod
    def display_roles(roles: dict) -> None:
        """
        Method to display the roles list.
        Args:
            roles (dict): The roles dictionary
        """
        click.echo("\nAll roles:")
        for role_id, role_name in roles.items():
            click.echo(f"  - {role_id}. {role_name.upper()}")

    @staticmethod
    def display_filters(filters: list) -> None:
        """
        Method to display the filters list.
        Args:
            filters (list): The filters list
        """
        click.echo("\nAll filters available :")
        for the_filter in filters:
            click.echo(f"  - {filters.index(the_filter) + 1}. {the_filter}")

    def display_filter_results(self, model_type: str,
                               my_filter: str,
                               filter_value: str | int | float,
                               results: list) -> None:
        """
        Method to display the filter results.
        Args:
            model_type (str): The model type.
            my_filter (str): The filter.
            filter_value (str | int | float): The filter value.
            results (list): The results.
        """
        click.echo("─" * 60)
        click.echo(f"All results for {model_type}s filtered by {my_filter} with '{filter_value}' value: ")
        click.echo("─"*60)
        click.echo("╌" * 50)
        for the_result in results:
            if (model_type.lower() == "manager" or model_type.lower() == "commercial"
                    or model_type.lower() == "technician" or model_type.lower() == "client"
                    or model_type.lower() == "event"):
                click.echo(f"  - {model_type.capitalize()} ❱ '{the_result.name}' : ")

            elif model_type.lower() == "contract" :
                click.echo(f"  - {model_type.capitalize()} ❱ n° {the_result.id} between '{the_result.client_name}' "
                           f"and '{the_result.commercial_name}'")

            click.echo("╌" * 50)
            actions = {
                "commercial": lambda : self.display_collaborator(collaborator=the_result, role="Commercial"),
                "manager": lambda : self.display_collaborator(collaborator=the_result, role="manager"),
                "technician": lambda : self.display_collaborator(collaborator=the_result, role="technician"),
                "contract": lambda : self.contract_view.display_contract(contract=the_result),
                "client": lambda : self.client_view.display_client(client=the_result),
                "event": lambda : self.event_view.display_event(event=the_result),
            }

            action = actions.get(model_type)
            action()
            click.echo("╌" * 50)
        click.echo("─" * 60)

    @staticmethod
    def display_filter_no_results(model_type: str, my_filter: str, filter_value: str | int | float) -> None:
        """
        Method to display when filtering results are empty.
        Args:
            model_type (str): The model type.
            my_filter (str): The filter.
            filter_value (str | int | float): The filter value.
        """
        if filter_value is not None :
            click.echo(f"\n❗ No results found for '{my_filter}' filtering in {model_type} "
                       f"with value '{filter_value}'.\n")

        else:
            click.echo(f"\n❗ No results found for '{my_filter}' filtering in {model_type}.\n")

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
                click.echo("❗ Please enter a number.")
                continue

            coll = (str(i+1) for i in range(nb))

            if answer not in coll:
                click.echo(f"❗ Please choose between 1 and {nb}.")
                continue

            return int(answer)

    def prompt_for_filter(self, filters: list) -> int | None:
        """
        Method to prompt the user to choose a filter
        Args:
            filters (list): The filters list

        Returns:
        The choice
        """

        self.display_filters(filters)

        answer = click.prompt(text="\n▶ Which filter do you want ? \n▶▶ ", type=int, default=1)

        return answer

    @staticmethod
    def prompt_for_filter_value(model_type: str, my_filter: str) -> str:
        """
        Method to prompt the user to choose a filter
        Args:
            model_type (str): The model type.
            my_filter (str): The filter.

        Returns:
        The string value
        """
        answer = click.prompt(text=f"\n▷▷ Type the value of '{my_filter}' filter for {model_type} "
                              f"or leave it blank if necessary : \n▶▶ ", type=str, default="")
        return answer

    @staticmethod
    def prompt_for_date_filter_value(model_type: str, my_filter: str) -> datetime | str:
        """
        Method to prompt the user to enter a date as filter value.
        Args:
            model_type (str): The model type.
            my_filter (str): The filter with which the user wants to filter the model_type.

        Returns:
        A datetime
        """
        while True:
            answer = click.prompt(text=f"\n▷▷ Type the value of '{my_filter}' filter for {model_type} (dd/mm/yy) "
                                       f"or leave it blank if necessary :\n▶▶ ",
                                  type=str,
                                  default="")
            if answer:
                try:
                    click.echo("ici")
                    return datetime.strptime(answer, '%d/%m/%y')

                except ValueError:
                    click.echo("❗ Please enter a valid date.")
            else:
                return ""

    @staticmethod
    def prompt_for_integer(model_type: str, my_filter: str) -> int:
        """
        Method to prompt the user to type integer
        Args:
            model_type (str): The model type.
            my_filter (int): The filter.

        Returns:
        The string value
        """
        answer = click.prompt(text=f"▷▷ Type the value of '{my_filter}' filter for {model_type}", type=int)
        return answer

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
        models = models.get("contracts") if model_type == "contract" else models

        answer = click.prompt(text=f"\n▶ Which {model_type} (from id {models[0].id} to id {models[-1].id}) do you want "
                                  f"to {action} ? \n▶▶ ", type=int, default=1)
        return answer

    @staticmethod
    def prompt_for_model_id(model_type: str, models: list | dict) -> int | None:
        """
        Method to prompt the user to choose an id in the models list.
        Args:
            model_type (str): The model type.
            models (list): The models list.

        Returns:
        The choice or None
        """
        click.echo(models)
        models = models.get("contracts") if isinstance(models, dict) else models
        click.echo(models)

        answer = click.prompt(text=f"\n▷▷ Please choose a {model_type} (from id {models[0].id} "
                              f"to id {models[-1].id}):\n▶▶ ", type=int, default=0)
        return answer

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
    def prompt_for_email() -> str | None:
        """
        Method to prompt the user the e-mail address.

        Returns:
        The e-mail address or None
        """
        while True:
            email = click.prompt(text=f"\n▷▷ Enter the e-mail address : \n▶▶ ", type=str)

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                click.echo("❗ Invalid e-mail address.")
                continue

            return email

    @staticmethod
    def prompt_for_password() -> str | None:
        """
        Method to prompt the user the password.
        Returns:
        The password or None
        """
        answer = click.prompt(text="\n▷▷ Enter the password : \n▶▶ ", type=str)
        return answer

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
            answer = click.prompt(text=f"\n▷▷ Are you sure you want to {action} this {model_type} (y/n) ?\n▶▶ ",
                                  type=str,
                                  default="n")

            if answer.lower() in ["y", "n"]:
                return True if answer.lower() == "y" else False

            click.echo(f"❗ Please enter either 'y' or 'n'.")

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
        answer = click.prompt(text=f"\n▷▷ Please type the {model_type} {field}:\n▶▶ ", type=str)
        return answer

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
        answer = click.prompt(text=f"\n▷▷ Please type the {model_type} {field} or leave blank to continue:\n▶▶ ",
                              type=str,
                              default="")
        return answer

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
            answer = click.prompt(text=f"\n▷▷ Please enter the {model_type} {field} (dd/mm/yy hh:mm) "
                                  f"or leave blank to continue:\n▶▶ ",
                                  type=str,
                                  default="")
            if answer:

                answer += ':00'

                try:
                    return datetime.strptime(answer, '%d/%m/%y %H:%M:%S')

                except ValueError:
                    click.echo("❗ Please enter a valid date.")
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
        email = self.prompt_for_email()

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

            role = click.prompt(text=f"\n▷▷ Which new role do you want to assign ? (1,2,3)\n▶▶ ", type=int, default=1)

            if role in [1,2,3]:
                return role, roles[role]

            click.echo("❗ Please enter an integer between 1 and 3.")
