import re
import sys
from datetime import datetime
from typing import Any

import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Commercial, Manager, Technician
from src.views.client_view import ClientView
from src.views.contract_view import ContractView
from src.views.event_view import EventView


class MainView:
    def __init__(self, console=None):
        self.console = console or Console(file=sys.stdout,
                                          force_terminal=True,
                                          color_system="truecolor",
                                          width=200,
                                          style="bright_white")

        self.contract_view = ContractView(self)
        self.client_view = ClientView(self)
        self.event_view = EventView(self)

    def display_main_menu(self) -> None:
        """
        Method to display the main menu.
        """
        self.console.print("\nWELCOME TO EPIC EVENTS !\n")
        self.console.print("▶ MAIN MENU ◀")
        self.console.print("▷▷ 1. Log in")
        self.console.print("▷▷ 2. Quit the app\n")

    def display_goodbye(self) -> None:
        """
        Method to display the goodbye message.
        """
        self.console.print("\n👋  Goodbye ! 👋\n")

    def display_logout(self) -> None:
        """
        Method to display the logout message.
        """
        self.console.print(Panel("\n✅ You are successfully logged out.\n",
                                 border_style="bold green",
                                 style="bold white",
                                 expand=False))

    def display_submenu(self, model_type) -> None:
        """
        Method to display the submenu.
        Args:
            model_type ():
        """
        self.console.print(f"\n▶ {model_type.upper()} MENU ◀\n")
        self.console.print("▷▷ 1. Display")
        self.console.print("▷▷ 2. Create")
        self.console.print("▷▷ 3. Update")
        self.console.print("▷▷ 4. Delete")
        self.console.print("▷▷ 5. Filter")
        self.console.print("▷▷ 6. Go back")

    def display_permission_denied(self, action: str, model_type: str) -> None:
        """
        Method to display the permission denied message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        self.console.print(Panel(f"❌[bold] You don't have the permission to [bold red]{action} "
                            f"a {model_type}[/bold].",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    def display_database_error(self):
        self.console.print(Panel(f"❗ Database error!.",
                                 border_style="bold red3",
                                 style="bold red3",
                                 expand=False))

    def display_error_while_filtering_value(self):
        self.console.print(Panel(f"❗ Error while filtering!.",
                                 border_style="bold red3",
                                 style="bold red3",
                                 expand=False))

    def display_date_format_error(self):
        self.console.print(Panel(f"❗ Try to format date fails!.",
                                 border_style="bold bright_red",
                                 style="bold red3",
                                 expand=False))

    def filtering_format_error(self):
        self.console.print(Panel(f"❗ Try to format filter fails!.",
                                 border_style="bold bright_red",
                                 style="bold red3",
                                 expand=False))

    def display_action_introduction(self, action: str, model_type: str) -> None:
        """
        Method to display the introduction message from an action.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        self.console.print(f"\n[bold light_goldenrod2]⭢ You are going to {action} {model_type}s.[/bold light_goldenrod2]\n")

    def display_login_submenu(self) -> None:
        """
        Method to display the submenu after login.
        """
        self.console.print("\n▶ LOG IN ◀\n")
        self.console.print("▷▷ You are going to enter the followings details :")
        self.console.print(" • your e-mail address")
        self.console.print(" • your password\n")

    def display_successfully_logged_in(self, name: str) -> None:
        """
        Method to display the successfully logged in message.
        Args:
            name (str): The name of the user.
        """
        self.console.print(Panel(f"\n✅ {name.capitalize()}, you are successfully logged in.\n",
                            border_style="bold green",
                            style="bold white",
                            expand=False))

    def display_error_while_logging_in(self) -> None:
        """
        Method to display the successfully logged in message.
        """
        self.console.print(Panel(f"\n❗ An unexpected error occurred while logging in.\n",
                            border_style="bold red3",
                            style="bold red3",
                            expand=False))

    def display_action_successfully_done(self, action: str, model_type: str) -> None:
        """
        Method to display the successfully done message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        self.console.print(Panel(f"\n✅ The {model_type} has been successfully {action}.\n",
                            border_style="bold green",
                            style="bold white",
                            expand=False))

    def display_action_fails(self, action: str, model_type: str) -> None:
        """
        Method to display the failure message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        self.console.print(Panel(f"\n❌ The [bold]{model_type}[/bold] has not been [bold]{action}[/bold].\n",
                            border_style="bold bright_red",
                            style="bold white",
                            expand=False))

    def display_not_connected(self) -> None:
        """
        Method to display when the user is not logged in.
        """
        self.console.print("\n❗ [bold bright_red]You need to log in first.[/bold bright_red]\n")

    def display_wrong_password(self) -> None:
        """
        Method to display the wrong password message.
        """
        self.console.print("\n❗ [bold bright_red]Invalid password.[/bold bright_red]\n")

    def display_collaborator_not_exists(self) -> None:
        """
        Method to display the message when a collaborator does not exist.
        """
        self.console.print("\n❗ [bold bright_red]This collaborator does not exist.[/bold bright_red]\n")

    def display_collaborator_menu(self) -> None:
        """
        Method to display the collaborator menu when successfully logged in.
        """
        self.console.print(f"\n▶ EPIC EVENTS - COLLABORATOR MENU ◀\n")
        self.console.print("▷▷ 1. Collaborator")
        self.console.print("▷▷ 2. Contract")
        self.console.print("▷▷ 3. Client")
        self.console.print("▷▷ 4. Event")
        self.console.print("▷▷ 5. Log out\n")

    def display_collaborator_submenu(self) -> None:
        """
        Method to display the collaborator submenu.
        """
        self.console.print(f"\n▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀\n")
        self.console.print("▷▷ 1. Manager")
        self.console.print("▷▷ 2. Commercial")
        self.console.print("▷▷ 3. Technician")
        self.console.print("▷▷ 4. Go back\n")

    def display_models(self, model_type: str, models: list) -> None:
        """
        Method to display the models list
        Args:
            model_type (str): The model type.
            models (list): The models list.
        """
        if (None,) in models or not models:
            if model_type == "contract":
                self.console.print(f"\n[bold red3] ⯀ {model_type.upper()}S[/bold red3] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            elif model_type == "client":
                self.console.print(f"\n[bold deep_sky_blue1] ⯀ {model_type.upper()}S[/bold deep_sky_blue1] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            elif model_type == "event":
                self.console.print(f"\n[bold spring_green3] ⯀ {model_type.upper()}S[/bold spring_green3] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            else:
                self.console.print(f"\n[bold grey85] ⯀ {model_type.upper()}S[/bold grey85] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

        else:
            if model_type == "contract":
                self.console.print(f"\n[bold red3] ⯀ {model_type.upper()}S TO DISPLAY : [/bold red3] \n")

            elif model_type == "client":
                self.console.print(f"\n[bold deep_sky_blue1] ⯀ {model_type.upper()}S TO DISPLAY : [/bold deep_sky_blue1] \n")

            elif model_type == "event":
                self.console.print(f"\n[bold spring_green3] ⯀ {model_type.upper()}S TO DISPLAY : [/bold spring_green3] \n")

            else:
                self.console.print(f"\n[bold grey85] ⯀ {model_type.upper()}S TO DISPLAY : [/bold grey85] \n")

            actions = {
                "contract": self.contract_view.display_contracts,
                "client": self.client_view.display_clients,
                "event": self.event_view.display_events,
                "manager": self.display_collaborators,
                "commercial": self.display_collaborators,
                "technician": self.display_collaborators,
            }

            action = actions.get(model_type)
            action(models)

    def display_collaborators(self, models: list) -> None:
        """
        Method to display the collaborators list.
        Args:
            models (list): The models list.
        """
        for model in models:
            self.console.print(Panel(f"  - {model.id}. {model.name.capitalize()}",
                                expand=False,
                                border_style="bold navajo_white3",
                                style="navajo_white3"))

    @staticmethod
    def collaborator_to_display(collaborator: type[Commercial | Manager | Technician], role: str) -> Panel:
        """
        Method to build the panel to display for the collaborator.
        Args:
            collaborator (type[Commercial] | type[Manager] | type[Technician]): The collaborator.
            role (str): The role of the collaborator.
        """
        table = Table(show_header=False, box=None, style="bright_white")
        table.add_row(f"[bold navajo_white3]Id[/bold navajo_white3] : {collaborator.id}")
        table.add_row(f"[bold navajo_white3]Name[/bold navajo_white3] : {collaborator.name}")
        table.add_row(f"[bold navajo_white3]Employee number[/bold navajo_white3] : {collaborator.employee_number}")
        table.add_row(f"[bold navajo_white3]E-mail[/bold navajo_white3] : {collaborator.email}")
        table.add_row(f"[bold navajo_white3]Role[/bold navajo_white3] : {role}")

        return Panel(table, border_style="bold navajo_white3", expand=False)

    def display_collaborator(self, collaborator: type[Commercial | Manager | Technician], role: str) -> None:
        """
        Method to display the collaborator.
        Args:
            collaborator (type[Commercial | Manager | Technician]): The collaborator.
            role (str): The role of the collaborator.
        """
        panel = self.collaborator_to_display(collaborator, role)
        self.console.print(panel)

    def display_title(self, model_type: str, model_id: int) -> None:
        """
        Method to display a title for a given model.
        Args:
            model_type (str): The model type.
            model_id (int): The model id.
        """
        self.console.print(f"\n[bright_white]Here is the {model_type} n°{model_id}: [/bright_white]\n")

    def display_model(self, model_type: str,
                      model: type[Client | Event | Contract]) -> None:
        """
        Method to display a model for a given type
        Args:
            model_type (str): The model type.
            model (type[Client] | type[Event] | type[Contract]): The model.
        """
        self.display_title(model_type, model.id)
        actions = {
            "contract": self.contract_view.display_contract,
            "client": self.client_view.display_client,
            "event": self.event_view.display_event
        }

        action = actions.get(model_type)
        panel = action(model)

        self.console.print(panel)

    def display_new_data_request(self, model_type: str, model_id: int) -> None:
        """
        Method to display a title for the new data request action for a given model type and model id.
        Args:
            model_type (str): The model type.
            model_id (int): The model id.
        """
        self.console.print(f"\n▶ Please enter the new data for the {model_type} n°{model_id}.")

    def display_model_already_exist(self, model_type: str) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            model_type (str): The model type.
        """
        self.console.print(Panel(f"\n❌ This [bold]{model_type}[/bold] already exists.\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    def display_collaborator_already_exists(self, collaborator: type[Commercial | Manager | Technician]) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            collaborator (type[Commercial | Manager | Technician]): The collaborator
        """
        self.console.print(Panel(f"\n❌ The collaborator [bold]{collaborator.email}[/bold] already exists.\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_collaborator_already_exists_but_inactive(collaborator: \
            type[Commercial | Manager | Technician]) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            collaborator (type[Commercial] | type[Manager] | type[Technician]): The collaborator
        """
        click.echo(f"\n❗ A collaborator inactive with this email [{collaborator.email}] already exists.\n")

    def display_something_wrong(self, action: str) -> None:
        """
        Method to display a message when something goes wrong during the givent action.
        """
        self.console.print(Panel(f"\n❌ Something went wrong while [bold]{action}[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    def display_something_wrong_while_creating(self) -> None:
        """
        Method to display a message when something goes wrong while creating
        """
        self.console.print(Panel(f"\n❌ Something went wrong while creating.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    def display_something_wrong_while_updating(self) -> None:
        """
        Method to display a message when something goes wrong while updating
        """
        self.console.print(Panel(f"\n❌ Something went wrong while updating.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    def display_something_wrong_while_deleting(self) -> None:
        """
        Method to display a message when something goes wrong while deleting
        """
        self.console.print(Panel(f"\n❌ Something went wrong while deleting.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    def display_action_impossible(self, action: str) -> None:
        """
        Method to display a message when the action is not possible.
        """
        self.console.print(Panel(f"\n❌ No models to [bold]{action}[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    def display_cannot_delete_admin_manager_or_yourself(self) -> None:
        """
        Method to display a message when a user wants to delete the admin manager or its own profile
        """
        self.console.print(Panel(f"\n❌ You can not [bold]delete[/bold] the [bold]admin[/bold] manager "
                            f"or your [bold]own account[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    def display_cannot_delete(self, model_type, model_linked) -> None:
        """
        Method to display when deletion is not possible
        Args:
            model_type (str): The model type.
            model_linked (str): The model type linked to the model
        """
        if model_type == "contract":
            self.console.print(Panel(f"\n❌ Cannot delete [bold]{model_type}[/bold] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bright_red",
                                style="white",
                                expand=False))

        elif model_type == "client":
            self.console.print(Panel(f"\n❌ Cannot delete "
                                f"[bold cornflower_blue]{model_type}[/bold cornflower_blue] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bright_red",
                                style="white",
                                expand=False))
        else:
            self.console.print(Panel(f"\n❌ Cannot delete "
                                f"[bold chartreuse2]{model_type}[/bold chartreuse2] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bold bright_red",
                                style="white",
                                expand=False))

    def display_wrong_collaborator_role(self):
        """
        Method to display a message when the user enters a wrong collaborator role.
        """
        self.console.print(Panel(f"\n❌ You did not enter a valid role as below : "
                            f"[manager | commercial | technician].\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    def display_roles(self, roles: dict) -> None:
        """
        Method to display the roles list.
        Args:
            roles (dict): The roles dictionary
        """
        self.console.print("[bold grey62]\nAll roles :[/bold grey62]")
        for role_id, role_name in roles.items():
            self.console.print(Panel(f"  - {role_id}. {role_name.upper()}"
                                f"[manager | commercial | technician].\n",
                                border_style="bold grey62",
                                style= "grey62",
                                expand=False))

    def display_filters(self, filters: list) -> None:
        """
        Method to display the filters list.
        Args:
            filters (list): The filters list
        """
        table = Table(
            title="All filters available".upper(),
            title_justify="center",
            show_header=False,
            expand=False,
            padding=(0, 5),
            border_style="bold pale_violet_red1",
            style="pale_violet_red1",
            title_style="bold pale_violet_red1",
            box = box.ROUNDED
        )
        table.add_column(header="\nAll filters available\n")

        for the_filter in filters:
            table.add_row(Panel(f"  - {filters.index(the_filter) + 1}. {the_filter}"
                                f"[manager | commercial | technician].\n",
                                border_style="bold pale_violet_red1",
                                style="pale_violet_red1",
                                expand=False,
                                height=3))

        self.console.print(table)

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
        self.console.print()
        title = Panel(
            f"[bold white]⮞ All results for {model_type}s filtered by {my_filter} "
            f"with value '{filter_value}' ⮜[/bold white]",
            border_style="bold white",
            expand=False
        )
        self.console.print(title)

        table = Table(
            show_header=False,
            box=box.MINIMAL,
            expand=False,
            padding=(0, 1),
            border_style="cyan",
        )

        for the_result in results:
            header = ""
            if (model_type.lower() == "manager" or model_type.lower() == "commercial"
                    or model_type.lower() == "technician"):
                header = Panel(f"[bold grey85]  - {model_type.upper()} ❱ '{the_result.name}' : [/bold grey85]",
                               border_style="",
                               expand=True)

            elif model_type.lower() == "contract" :
                header = Panel(f"[bold bright_red]  - {model_type.upper()} ❱ n° {the_result.id} "
                               f"between '{the_result.client_name}' "
                               f"and '{the_result.commercial_name}'[/bold bright_red]",
                               border_style="bold bright_red",
                               expand=True)

            elif model_type.lower() == "client" :
                header = Panel(f"[bold deep_sky_blue1]  - {model_type.upper()} ❱ n° {the_result.id} [/bold deep_sky_blue1]"
                               f"[deep_sky_blue1]- '{the_result.name}' [/deep_sky_blue1]",
                               border_style="bold deep_sky_blue1",
                               expand=True)

            elif model_type.lower() == "event" :
                header = Panel(f"[bold spring_green3]  - {model_type.upper()} ❱ n° {the_result.id} [/bold spring_green3]"
                               f"[spring_green3]- '{the_result.name}' [/spring_green3]",
                               border_style="bold spring_green3",
                               expand=True)

            table.add_row(header)

            actions = {
                "commercial": lambda : self.collaborator_to_display(collaborator=the_result, role="Commercial"),
                "manager": lambda : self.collaborator_to_display(collaborator=the_result, role="manager"),
                "technician": lambda : self.collaborator_to_display(collaborator=the_result, role="technician"),
                "contract": lambda : self.contract_view.display_contract(contract=the_result),
                "client": lambda : self.client_view.display_client(client=the_result),
                "event": lambda : self.event_view.display_event(event=the_result),
            }

            action = actions.get(model_type)
            details = action()
            table.add_row(details)
            table.add_row("")
            table.add_row("[grey46]-[/grey46]" * 60)
            table.add_row("")

        self.console.print(table)

    def display_filter_no_results(self, model_type: str, my_filter: str, filter_value: str | int | float) -> None:
        """
        Method to display when filtering results are empty.
        Args:
            model_type (str): The model type.
            my_filter (str): The filter.
            filter_value (str | int | float): The filter value.
        """
        if filter_value is not None :
            self.console.print(f"\n❗ [bright_red]No results found for [bold]'{my_filter}'[/bold] filtering "
                          f"in [bold]{model_type}s[/bold] "
                          f"with value [bold]'{filter_value}'[/bold].[/bright_red]\n")

        else:
            self.console.print(f"\n❗ [bright_red]No results found for [bold]'{my_filter}'[/bold] filtering "
                          f"in [bold]{model_type}[/bold].[/bright_red]\n")

    def prompt_for_menu(self, nb) -> int | None:
        """
        Method to prompt the user to choose the action in the menu
        Args:
            nb (int): The number of choice.

        Returns:
        The choice
        """
        while True:
            answer = Prompt.ask("\n[bold light_goldenrod2]▶ What do you want to do ?[/bold light_goldenrod2]\n"
                                "▶▶ ")

            if not answer.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i+1) for i in range(nb))

            if answer not in coll:
                self.console.print(f"\n❗ [bold bright_red]Please choose between 1 and {nb}.\n[/bold bright_red]")
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
        while True:
            self.display_filters(filters)

            answer = Prompt.ask("[bold light_goldenrod2]\n▶ Which filter do you want ? [/bold light_goldenrod2]\n"
                                "▶▶ ")

            if not answer.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(filters)))

            if answer not in coll:
                self.console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(filters)}.\n[/bold bright_red]")
                continue

            return int(answer)

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
        answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Type the value of '{my_filter}' filter for {model_type} "
                            f"or leave it blank if necessary [/bold light_goldenrod2]\n"
                            f"▶▶ ", default="")
        return answer

    def prompt_for_date_filter_value(self, model_type: str, my_filter: str) -> datetime | str:
        """
        Method to prompt the user to enter a date as filter value.
        Args:
            model_type (str): The model type.
            my_filter (str): The filter with which the user wants to filter the model_type.

        Returns:
        A datetime
        """
        while True:
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Type the value of '{my_filter}' filter for "
                                f"{model_type} (dd/mm/yy) "
                                f"or leave it blank if necessary[/bold light_goldenrod2]\n"
                                f"▶▶ ",
                                default="")
            if answer:
                try:
                    return datetime.strptime(answer, '%d/%m/%y')

                except ValueError:
                    self.console.print("❗ [bold bright_red]Please enter a valid date.[/bold bright_red]")

            return ""

    def prompt_for_integer(self, model_type: str, my_filter: str) -> int | None:
        """
        Method to prompt the user to type integer
        Args:
            model_type (str): The model type.
            my_filter (str): The filter.

        Returns:
        The integer value
        """
        while True:
            answer = Prompt.ask(f"[bold light_goldenrod2]▷▷ Type the value of '{my_filter}' filter for {model_type}"
                                f"[bold light_goldenrod2]")

            if not answer.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            return int(answer)

    def prompt_for_model_id_with_action(self, action: str, model_type: str, models: dict) -> int | None:
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
            models = models.get("contracts") if model_type == "contract" else models

            answer = Prompt.ask(f"\n[bold light_goldenrod2]▶ Which {model_type} "
                                f"(from id {models[0].id} to id {models[-1].id}) do you want "
                                f"to {action} ?[/bold light_goldenrod2] \n"
                                f"▶▶ ", default="1")

            if not answer.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(models)))

            if answer not in coll:
                self.console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(models)}."
                                   f"\n[/bold bright_red]")
                continue

            return int(answer)

    def prompt_for_model_id(self, model_type: str, models: list | dict) -> int | None:
        """
        Method to prompt the user to choose an id in the models list.
        Args:
            model_type (str): The model type.
            models (list): The models list.

        Returns:
        The choice
        """
        while True:
            models = models.get("contracts") if isinstance(models, dict) else models

            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please choose a {model_type} "
                                f"(from id {models[0].id} "
                                f"to id {models[-1].id})[/bold light_goldenrod2]\n"
                                f"▶▶ ", default="1")

            if not answer.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(models)))

            if answer not in coll:
                self.console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(models)}."
                                   f"\n[/bold bright_red]")
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
            input_key = Prompt.ask("[bold light_goldenrod2]▷▷ Type 'q' to go back or anything else to continue "
                                   "[/bold light_goldenrod2]\n"
                                   "▶▶ ")
            return input_key.lower()

    def prompt_for_email(self) -> str | None:
        """
        Method to prompt the user the e-mail address.

        Returns:
        The e-mail address or None
        """
        while True:
            email = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Enter the e-mail address [/bold light_goldenrod2]\n"
                               f"▶▶ ")

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                self.console.print("❗ [bold bright_red]Invalid e-mail address.[/bold bright_red]")
                continue

            return email

    @staticmethod
    def prompt_for_password() -> str | None:
        """
        Method to prompt the user the password.
        Returns:
        The password or None
        """
        answer = Prompt.ask("\n[bold light_goldenrod2]▷▷ Enter the password[/bold light_goldenrod2] \n"
                            "▶▶ ")
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
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Are you sure you want to {action} this "
                                f"{model_type} (y/n) ?[/bold light_goldenrod2]\n"
                                f"▶▶ ",
                                  default="n")

            if answer.lower() in ["y", "n"]:
                return True if answer.lower() == "y" else False

            click.echo(f"❗ [bold bright_red]Please enter either 'y' or 'n'.[/bold bright_red]")

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
        answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please type the {model_type} {field}:"
                            f"[/bold light_goldenrod2]\n"
                            f"▶▶ ")
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
        answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please type the {model_type} {field} or leave blank to continue"
                            f"[/bold light_goldenrod2]\n"
                            f"▶▶ ",
                            default="")
        return answer

    def prompt_for_date(self, model_type: str, field: str) -> datetime | None:
        """
        Method to prompt the user to enter a date
        Args:
            model_type (str): The model type.
            field (str): The date field to be entered.

        Returns:
        A datetime or None
        """
        while True:
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please enter the {model_type} {field} (dd/mm/yy hh:mm) "
                                f"or leave blank to continue[/bold light_goldenrod2]\n"
                                f"▶▶ ",
                                default="")
            if answer:

                answer += ':00'

                try:
                    return datetime.strptime(answer, '%d/%m/%y %H:%M:%S')

                except ValueError:
                    self.console.print("❗ [bold bright_red]Please enter a valid date.[/bold bright_red]")
            else:
                return None

    def prompt_for_collaborator(self, role) -> tuple[str | None, str | None, str]:
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

    def prompt_for_collaborator_role(self) -> tuple[int, Any | None] | None:
        """
        Method to prompt the user to enter the collaborator role

        Returns:
        A tuple with the role id and the role of the collaborator.
        """
        while True:
            roles = {
                1: "manager",
                2: "commercial",
                3: "technician",
            }
            self.display_roles(roles)

            role = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Which new role do you want to assign, "
                              f"if wanted? (1,2,3)[/bold light_goldenrod2]\n"
                              f"▶▶ ")

            if not role.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            if int(role) not in roles:
                self.console.print("\n❗ [bold bright_red]Please enter an integer between 1 and 3.\n"
                                   "[/bold bright_red]")
                continue

            return int(role), str(roles.get(int(role)))

    def prompt_for_collaborator_role_to_action(self, action) -> str | None:
        """
        Method to prompt the user to enter the collaborator role

        Returns:
        The role.
        """
        while True:
            roles = {
                1: "manager",
                2: "commercial",
                3: "technician",
            }
            self.display_roles(roles)

            role = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Which collaborator do you want to {action}? "
                              f"(1,2,3)[/bold light_goldenrod2]\n"
                              f"▶▶ ")

            if not role.isdigit():
                self.console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            role = int(role)
            if role not in roles:
                self.console.print("\n❗ [bold bright_red]Please enter an integer between 1 and 3.\n"
                                   "[/bold bright_red]")
                continue

            return roles.get(role)
