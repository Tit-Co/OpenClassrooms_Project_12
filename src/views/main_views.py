import re
from src.views.contract_views import ContractView


class MainView:
    def __init__(self):
        self.contract_view = ContractView(self)

    @staticmethod
    def display_main_menu():
        print("\nWELCOME TO EPIC EVENTS !\n")
        print("▶ MAIN MENU ◀")
        print("▷▷ 1. Log in")
        print("▷▷ 2. Quit the app\n")

    @staticmethod
    def display_goodbye():
        print("\n👋  Goodbye ! 👋\n")

    @staticmethod
    def display_logout():
        print("\nYou are successfully logged out.\n")

    @staticmethod
    def display_submenu(model_type):
        print(f"\n▶ {model_type.upper()} MENU ◀\n")
        print("▷▷ 1. Display")
        print("▷▷ 2. Create")
        print("▷▷ 3. Update")
        print("▷▷ 4. Delete")
        print("▷▷ 5. Filter")
        print("▷▷ 6. Go back")

    @staticmethod
    def display_permission_denied(action, model_type):
        print(f"You don't have permission to {action} a {model_type}.")

    @staticmethod
    def display_action(action, model_type):
        print(f"You are going to {action} a {model_type}.")

    @staticmethod
    def display_login_submenu():
        print("\n▶ LOG IN ◀\n")
        print("▷▷ You are going to enter the followings details :")
        print(" • your e-mail address")
        print(" • your password\n")

    @staticmethod
    def display_successfully_logged_in(name):
        print(f"\n{name.capitalize()}, you are successfully logged in.\n")

    @staticmethod
    def display_action_successfully_done(action, model_type):
        print(f"\nThe {model_type} has been successfully {action}.\n")

    @staticmethod
    def display_wrong_password():
        print("Invalid password.")

    @staticmethod
    def display_collaborator_does_not_exist():
        print("This collaborator does not exist.")

    @staticmethod
    def display_collaborator_menu():
        print(f"\n▶ EPIC EVENTS - COLLABORATOR MENU ◀\n")
        print("▷▷ 1. Collaborator")
        print("▷▷ 2. Contract")
        print("▷▷ 3. Client")
        print("▷▷ 4. Event")
        print("▷▷ 5. Log out\n")

    @staticmethod
    def display_collaborator_submenu():
        print(f"\n▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀\n")
        print("▷▷ 1. Manager")
        print("▷▷ 2. Commercial")
        print("▷▷ 3. Technician")
        print("▷▷ 4. Go back\n")

    def display_models(self, model_type, models):
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
                "technician": self.display_collaborators
            }

            action = actions.get(model_type)
            action(models)

    @staticmethod
    def display_clients_events(models):
        for model in models:
            print(f"  - {model.id}. {model.name}")

    @staticmethod
    def display_collaborators(models):
        for model in models:
            print(f"  - {model.id}. {model.name.capitalize()}")

    @staticmethod
    def display_collaborator(collaborator):
        print(f"\nHere is the required collaborator :\n")
        print(f"Id : {collaborator.id}")
        print(f"Name : {collaborator.name}")
        print(f"Email : {collaborator.email}")
        print(f"Role: {collaborator.role_name}")

    @staticmethod
    def display_title(model_type):
        print(f"\nHere is the {model_type} : \n")

    def display_model(self, model_type, model):
        self.display_title(model_type)
        actions = {
            "contract": self.contract_view.display_contract,
            "client": self.display_client,
            "event": self.display_event,
        }

        action = actions.get(model_type)
        action(model)

    @staticmethod
    def display_client(model):
        print(f"Id : {model.id}")
        print(f"Name : {model.name}")
        print(f"Email : {model.email}")
        print(f"Phone : {model.phone}")
        print(f"Company : {model.company}")
        print(f"Creation date : {model.creation_date}")
        print(f"Last update : {model.last_update}")
        print(f"Commercial name : {model.commercial_name}")

    @staticmethod
    def display_event(model):
        print(f"Id : {model.id}")
        print(f"Name : {model.name}")
        print(f"Client name : {model.client_name}")
        print(f"Client email : {model.client_email}")
        print(f"Client phone : {model.client_phone}")
        print(f"Start date : {model.start_date}")
        print(f"End date : {model.end_date}")
        print(f"Support contact : {model.technician_name}")
        print(f"Location : {model.location}")
        print(f"Attendees : {model.attendees}")
        print(f"Notes : {model.notes}")

    @staticmethod
    def display_new_data_request(model_type, model_id):
        print(f"\n▶ Please enter the new data for the {model_type} n°{model_id}.")

    @staticmethod
    def prompt_for_menu(nb):
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
    def prompt_for_model_id_with_action(action, model_type, models):
        while True:
            coll = [model.id for model in models]
            answer = input(f"\n▶ Which {model_type} do you want to {action} ? \n▶▶ ")

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            if int(answer) not in coll:
                print(f"Please choose a number from id {models[0].id} to id {models[-1].id}.")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_model_id(model_type, models):
        while True:
            coll = [model.id for model in models]

            answer = input(f"\n▶ Please choose a {model_type} :\n▶▶ ").strip()

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            if int(answer) not in coll:
                print(f"Please choose a number from id {models[0].id} to id {models[-1].id}.")
                continue

            return int(answer)

    @staticmethod
    def prompt_for_continuing():
        while True:
            input_key = input("▷▷ Type 'q' to go back or anything else to continue : \n▶▶ ")
            return input_key.lower()

    @staticmethod
    def prompt_for_email():
        while True:
            email = input("\n▶ Enter the e-mail address : \n▶▶ ")

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                print("Invalid e-mail address.")
                continue

            return email

    @staticmethod
    def prompt_for_password():
        return input("\n▶ Enter the password : \n▶▶ ")

    @staticmethod
    def prompt_for_confirmation(action, model_type):
        while True:
            answer = input(f"\n▷▷ Are you sure you want to {action} this {model_type} (y/n) ?\n▶▶ ")

            if answer.lower() in ["y", "n"]:
                return True if answer.lower() == "y" else False

            print(f"Please enter either 'y' or 'n'.")
