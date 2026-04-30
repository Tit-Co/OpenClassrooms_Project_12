import click
import re
import sys

from datetime import datetime

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


console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200,
    style="bright_white"
)


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
        console.print(Panel("\n✅ You are successfully logged out.\n",
                            border_style="bold green",
                            style="bold white",
                            expand=False))

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
        console.print(Panel(f"❌ You don't have the permission to [bold red]{action}[/bold red] "
                            f"a [bold red]{model_type}[/bold red].",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_action_introduction(action: str, model_type: str) -> None:
        """
        Method to display the introduction message from an action.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        console.print(f"\n[bold light_goldenrod2]⭢ You are going to {action} {model_type}s.[/bold light_goldenrod2]\n")

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
        console.print(Panel(f"\n✅ {name.capitalize()}, you are successfully logged in.\n",
                            border_style="bold green",
                            style="bold white",
                            expand=False))

    @staticmethod
    def display_action_successfully_done(action: str, model_type: str) -> None:
        """
        Method to display the successfully done message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        console.print(Panel(f"\n✅ The {model_type} has been successfully {action}.\n",
                            border_style="bold green",
                            style="bold white",
                            expand=False))

    @staticmethod
    def display_action_fails(action: str, model_type: str) -> None:
        """
        Method to display the failure message.
        Args:
            action (str): The action.
            model_type (str): The model type.
        """
        console.print(Panel(f"\n❌ The [bold]{model_type}[/bold] has not been [bold]{action}[/bold].\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_not_connected() -> None:
        """
        Method to display when the user is not logged in.
        """
        console.print("❗ [bold bright_red]You need to log in first.[/bold bright_red]")

    @staticmethod
    def display_wrong_password() -> None:
        """
        Method to display the wrong password message.
        """
        console.print("❗ [bold bright_red]Invalid password.[/bold bright_red]")

    @staticmethod
    def display_collaborator_not_exists() -> None:
        """
        Method to display the message when a collaborator does not exist.
        """
        console.print("❗ [bold bright_red]This collaborator does not exist.[/bold bright_red]")

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
            if model_type == "contract":
                console.print(f"\n[bold red3] ⯀ {model_type.upper()}S[/bold red3] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            elif model_type == "client":
                console.print(f"\n[bold deep_sky_blue1] ⯀ {model_type.upper()}S[/bold deep_sky_blue1] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            elif model_type == "event":
                console.print(f"\n[bold spring_green3] ⯀ {model_type.upper()}S[/bold spring_green3] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

            else:
                console.print(f"\n[bold grey85] ⯀ {model_type.upper()}S[/bold grey85] "
                              f"- [gold3]No {model_type} to display.[/gold3]\n")

        else:
            if model_type == "contract":
                console.print(f"\n[bold red3] ⯀ {model_type.upper()}S TO DISPLAY : [/bold red3] \n")

            elif model_type == "client":
                console.print(f"\n[bold deep_sky_blue1] ⯀ {model_type.upper()}S TO DISPLAY : [/bold deep_sky_blue1] \n")

            elif model_type == "event":
                console.print(f"\n[bold spring_green3] ⯀ {model_type.upper()}S TO DISPLAY : [/bold spring_green3] \n")

            else:
                console.print(f"\n[bold grey85] ⯀ {model_type.upper()}S TO DISPLAY : [/bold grey85] \n")

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

    @staticmethod
    def display_collaborators(models: list) -> None:
        """
        Method to display the collaborators list.
        Args:
            models (list): The models list.
        """
        for model in models:
            console.print(Panel(f"  - {model.id}. {model.name.capitalize()}",
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
        table.add_row(f"[bold navajo_white3]name[/bold navajo_white3] : {collaborator.name}")
        table.add_row(f"[bold navajo_white3]Employee number[/bold navajo_white3] : {collaborator.employee_number}")
        table.add_row(f"[bold navajo_white3]E-mail[/bold navajo_white3] : {collaborator.email}")

        return Panel(table, border_style="bold navajo_white3", expand=False)

    def display_collaborator(self, collaborator: type[Commercial | Manager | Technician], role: str) -> None:
        """
        Method to display the collaborator.
        Args:
            collaborator (type[Commercial | Manager | Technician]): The collaborator.
            role (str): The role of the collaborator.
        """
        panel = self.collaborator_to_display(collaborator, role)
        console.print(panel)

    @staticmethod
    def display_title(model_type: str, model_id: int) -> None:
        """
        Method to display a title for a given model.
        Args:
            model_type (str): The model type.
            model_id (int): The model id.
        """
        console.print(f"\n[bright_white]Here is the {model_type} n°{model_id}: [/bright_white]\n")

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

        console.print(panel)

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
        console.print(Panel(f"\n❌ This [bold]{model_type}[/bold] already exists.\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_collaborator_already_exists(collaborator: type[Commercial | Manager | Technician]) -> None:
        """
        Method to display a message when a model already exists.
        Args:
            collaborator (type[Commercial | Manager | Technician]): The collaborator
        """
        console.print(Panel(f"\n❌ The collaborator [bold]{collaborator.email}[/bold] already exists.\n",
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

    @staticmethod
    def display_something_wrong(action: str) -> None:
        """
        Method to display a message when something goes wrong during the givent action.
        """
        console.print(Panel(f"\n❌ Something went wrong while [bold]{action}[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_something_wrong_while_creating() -> None:
        """
        Method to display a message when something goes wrong while creating
        """
        console.print(Panel(f"\n❌ Something went wrong while creating.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))
        
    @staticmethod
    def display_something_wrong_while_updating() -> None:
        """
        Method to display a message when something goes wrong while updating
        """
        console.print(Panel(f"\n❌ Something went wrong while updating.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_something_wrong_while_deleting() -> None:
        """
        Method to display a message when something goes wrong while deleting
        """
        console.print(Panel(f"\n❌ Something went wrong while deleting.\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_action_impossible(action: str) -> None:
        """
        Method to display a message when the action is not possible.
        """
        console.print(Panel(f"\n❌ No models to [bold]{action}[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_cannot_delete_admin_manager_or_yourself() -> None:
        """
        Method to display a message when a user wants to delete the admin manager or its own profile
        """
        console.print(Panel(f"\n❌ You can not [bold]delete[/bold] the [bold]admin[/bold] manager "
                            f"or your [bold]own account[/bold].\n",
                            border_style="bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_cannot_delete(model_type, model_linked) -> None:
        """
        Method to display when deletion is not possible
        Args:
            model_type (str): The model type.
            model_linked (str): The model type linked to the model
        """
        if model_type == "contract":
            console.print(Panel(f"\n❌ Cannot delete [bold]{model_type}[/bold] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bright_red",
                                style="white",
                                expand=False))

        elif model_type == "client":
            console.print(Panel(f"\n❌ Cannot delete "
                                f"[bold cornflower_blue]{model_type}[/bold cornflower_blue] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bright_red",
                                style="white",
                                expand=False))
        else:
            console.print(Panel(f"\n❌ Cannot delete "
                                f"[bold chartreuse2]{model_type}[/bold chartreuse2] : {model_linked}(s) "
                                f"linked.\n",
                                border_style="bold bright_red",
                                style="white",
                                expand=False))

    @staticmethod
    def display_wrong_collaborator_role():
        """
        Method to display a message when the user enters a wrong collaborator role.
        """
        console.print(Panel(f"\n❌ You did not enter a valid role as below : "
                            f"[manager | commercial | technician].\n",
                            border_style="bold bright_red",
                            style="white",
                            expand=False))

    @staticmethod
    def display_roles(roles: dict) -> None:
        """
        Method to display the roles list.
        Args:
            roles (dict): The roles dictionary
        """
        console.print("[bold gray62]\nAll roles :[/bold grey62]")
        for role_id, role_name in roles.items():
            console.print(Panel(f"  - {role_id}. {role_name.upper()}"
                                f"[manager | commercial | technician].\n",
                                border_style="bold grey62",
                                style= "grey62",
                                expand=False))

    @staticmethod
    def display_filters(filters: list) -> None:
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

        console.print(table)

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
        click.echo()
        title = Panel(
            f"[bold white]⮞ All results for {model_type}s filtered by {my_filter} "
            f"with value '{filter_value}' ⮜[/bold white]",
            border_style="bold white",
            expand=False
        )
        console.print(title)

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

        console.print(table)

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
            console.print(f"\n❗ [bright_red]No results found for [bold]'{my_filter}'[/bold] filtering "
                          f"in [bold]{model_type}s[/bold] "
                          f"with value [bold]'{filter_value}'[/bold].[/bright_red]\n")

        else:
            console.print(f"\n❗ [bright_red]No results found for [bold]'{my_filter}'[/bold] filtering "
                          f"in [bold]{model_type}[/bold].[/bright_red]\n")

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
            answer = Prompt.ask("\n[bold light_goldenrod2]▶ What do you want to do ?[/bold light_goldenrod2]\n"
                                "▶▶ ")

            if not answer.isdigit():
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i+1) for i in range(nb))

            if answer not in coll:
                console.print(f"\n❗ [bold bright_red]Please choose between 1 and {nb}.\n[/bold bright_red]")
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
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(filters)))

            if answer not in coll:
                console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(filters)}.\n[/bold bright_red]")
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
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Type the value of '{my_filter}' filter for {model_type} (dd/mm/yy) "
                                f"or leave it blank if necessary[/bold light_goldenrod2]\n"
                                f"▶▶ ",
                                default="")
            if answer:
                try:
                    return datetime.strptime(answer, '%d/%m/%y')

                except ValueError:
                    console.print("❗ [bold bright_red]Please enter a valid date.[/bold bright_red]")
            else:
                return ""

    @staticmethod
    def prompt_for_integer(model_type: str, my_filter: str) -> int | None:
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
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
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
            models = models.get("contracts") if model_type == "contract" else models

            answer = Prompt.ask(f"\n[bold light_goldenrod2]▶ Which {model_type} (from id {models[0].id} to id {models[-1].id}) do you want "
                                f"to {action} ?[/bold light_goldenrod2] \n"
                                f"▶▶ ", default=1)

            if not answer.isdigit():
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(models)))

            if answer not in coll:
                console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(models)}.\n[/bold bright_red]")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_model_id(model_type: str, models: list | dict) -> int | None:
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

            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please choose a {model_type} (from id {models[0].id} "
                                f"to id {models[-1].id})[/bold light_goldenrod2]\n"
                                f"▶▶ ", default=1)

            if not answer.isdigit():
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            coll = (str(i + 1) for i in range(len(models)))

            if answer not in coll:
                console.print(f"\n❗ [bold bright_red]Please choose between 1 and {len(models)}.\n[/bold bright_red]")
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

    @staticmethod
    def prompt_for_email() -> str | None:
        """
        Method to prompt the user the e-mail address.

        Returns:
        The e-mail address or None
        """
        while True:
            email = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Enter the e-mail address [/bold light_goldenrod2]\n"
                               f"▶▶ ")

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                console.print("❗ [bold bright_red]Invalid e-mail address.[/bold bright_red]")
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
            answer = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Please enter the {model_type} {field} (dd/mm/yy hh:mm) "
                                f"or leave blank to continue[/bold light_goldenrod2]\n"
                                f"▶▶ ",
                                default="")
            if answer:

                answer += ':00'

                try:
                    return datetime.strptime(answer, '%d/%m/%y %H:%M:%S')

                except ValueError:
                    console.print("❗ [bold bright_red]Please enter a valid date.[/bold bright_red]")
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

    def prompt_for_collaborator_role(self, roles: dict) -> tuple[int, str] | None:
        """
        Method to prompt the user to enter the collaborator role
        Args:
            roles (list): The roles available for the collaborator.

        Returns:
        A tuple with the role id and the role of the collaborator.
        """
        while True:
            self.display_roles(roles)

            role = Prompt.ask(f"\n[bold light_goldenrod2]▷▷ Which new role do you want to assign ? (1,2,3)"
                              f"[/bold light_goldenrod2]\n"
                              f"▶▶ ",
                              default=1)

            if not role.isdigit():
                console.print("\n❗ [bold bright_red]Please enter a number.\n[/bold bright_red]")
                continue

            if int(role) not in [1,2,3]:
                console.print("❗ [bold bright_red]Please enter an integer between 1 and 3.[/bold bright_red]")

            return int(role), roles[int(role)]
