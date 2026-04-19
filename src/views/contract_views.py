class ContractView:
    def __init__(self, main_view):
        self.main_view = main_view

    @staticmethod
    def is_float(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def display_contracts(models):
        for model in models:
            print(f"  - Contract n° {model.id}")

    @staticmethod
    def display_contract(contract):
        print(f"Id : {contract.id}")
        print(f"Client name : {contract.client_name}")
        print(f"Client email : {contract.client_email}")
        print(f"Client phone : {contract.client_phone}")
        print(f"Commercial name : {contract.commercial_name}")
        print(f"Total amount : {contract.total_amount} $")
        print(f"Bill to pay : {contract.bill_to_pay} $")
        print(f"Creation date : {contract.creation_date}")
        print(f"Contract signed : {'✅' if contract.status else '❌'}")

    def prompt_for_contract(self, clients, commercials):
        self.main_view.display_models("client", clients)
        client_id = self.prompt_for_id("client")

        self.main_view.display_models("commercial", commercials)
        commercial_id = self.prompt_for_id("commercial")

        total_amount = self.prompt_for_contract_float_number("total_amount")

        bill_to_pay = self.prompt_for_contract_float_number("bill_to_pay")

        status = self.prompt_for_contract_boolean()

        return client_id, commercial_id, total_amount, bill_to_pay, status

    @staticmethod
    def prompt_for_id(model_type):
        while True:
            answer = input(f"\n▶ Please select a {model_type} for the contract if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

    def prompt_for_contract_float_number(self, model_type):
        while True:
            if model_type == "total_amount":
                answer = input("\n▶ Please type the contract total amount if possible:\n▶▶ ").strip()
            else:
                answer = input("\n▶ Please type the amount left to pay if existing:\n▶▶ ").strip()

            if self.is_float(answer) or answer.isdigit() or answer == "":
                return float(answer) if answer else None

            print(f"Please enter a number or leave blank to continue.")

    @staticmethod
    def prompt_for_contract_boolean():
        while True:
            status = input("\n▶ Is the contract signed (y/n):\n▶▶ ")

            if status.lower() in ["y", "n"]:
                return status == "y"

            print(f"Please enter either 'y' or 'n'.")
