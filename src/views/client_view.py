class ClientView:
    def __init__(self, main_view):
        self.main_view = main_view

    def display_client(self, client):
        self.main_view.display_title(model_type="client")
        print(f"Id : {client.id}")
        print(f"name : {client.name}")
        print(f"E-mail : {client.email}")
        print(f"Phone : {client.phone}")
        print(f"Company : {client.company}")
        print(f"Creation date : {client.creation_date}")
        print(f"Last update : {client.last_update}")
        print(f"Commercial name : {client.commercial_name or ''}")

    def prompt_for_client(self, commercials):
        self.main_view.display_models("commercial", commercials)
        client_id = self.prompt_for_id(model_type="commercial")

        name = self.main_view.prompt_for_string(model_type="client", field="name")

        email = self.prompt_for_client_email()

        phone = self.main_view.prompt_for_string_if_known(model_type="client", field="phone")

        company =  self.main_view.prompt_for_string_if_known(model_type="client", field="company")

        return client_id, name, email, phone, company

    @staticmethod
    def prompt_for_id(model_type):
        while True:
            answer = input(f"\n▶ Please select a {model_type} for the client if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

    def prompt_for_client_email(self):
        return self.main_view.prompt_for_email(model_type=" client")
