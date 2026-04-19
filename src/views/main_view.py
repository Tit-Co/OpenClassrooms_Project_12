import re


class MainView:
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
        print("▷▷ 1. Administrator")
        print("▷▷ 2. Commercial")
        print("▷▷ 3. Technician")
        print("▷▷ 4. Go back\n")

    def display_models(self, model_type, models):
        if not models:
            print(f"\nNo {model_type} to display.\n")
        else:
            print(f"\nHere are all the {model_type}s : \n")

            actions = {
                "contract": self.display_contracts,
                "client": self.display_clients_events,
                "event": self.display_clients_events,
                "administrator": self.display_collaborators,
                "commercial": self.display_collaborators,
                "technician": self.display_collaborators
            }

            action = actions.get(model_type)
            action(models)

    @staticmethod
    def display_contracts(models):
        for model in models:
            print(f"Contract n° {model.id}")

    @staticmethod
    def display_clients_events(models):
        for model in models:
            print(f"{model.id}. {model.name}")

    @staticmethod
    def display_collaborators(models):
        for model in models:
            print(f"{model.id}. {model.name.capitalize()}")

    @staticmethod
    def display_collaborator(collaborator):
        print(f"\nHere is the required collaborator :\n")
        print(f"Id : {collaborator.id}")
        print(f"Name : {collaborator.name}")
        print(f"Email : {collaborator.email}")
        print(f"Role: {collaborator.role_name}")

    def display_model(self, model_type, model):
        print(f"\nHere is the {model_type} : \n")
        actions = {
            "contract": self.display_contract,
            "client": self.display_client,
            "event": self.display_event,
        }

        action = actions.get(model_type)
        action(model)

    @staticmethod
    def display_contract(model):
        print(f"Id : {model.id}")
        print(f"Client name : {model.client_name}")
        print(f"Client email : {model.client_email}")
        print(f"Client phone : {model.client_phone}")
        print(f"Total amount : {model.total_amount} $")
        print(f"Bill to pay : {model.bill_to_pay} $")
        print(f"Creation date : {model.creation_date}")
        print(f"Contract signed : {'✅' if model.status else '❌'}")

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
    def prompt_for_model(nb, action, model_type):
        while True:
            answer = input(f"\n▶ Which {model_type} do you want to {action} ? \n▶▶ ")

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            coll = (str(i + 1) for i in range(nb))
            if answer not in coll:
                print(f"Please choose between 1 and {nb}.")
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
