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

    def display_contract(self, contract):
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

    def prompt_for_contract(self, clients, commercials):
        self.main_view.display_models(model_type="client", models=clients)
        client_id = self.prompt_for_id(model_type="client")

        self.main_view.display_models(model_type="commercial", models=commercials)
        commercial_id = self.prompt_for_id(model_type="commercial")

        total_amount = self.prompt_for_contract_float_number(amount_type="total_amount")

        bill_to_pay = self.prompt_for_contract_float_number(amount_type="bill_to_pay")

        status = self.prompt_for_contract_boolean()

        return client_id, commercial_id, total_amount, bill_to_pay, status

    @staticmethod
    def prompt_for_id(model_type):
        while True:
            answer = input(f"\n▶ Please select a {model_type} for the contract if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

    def prompt_for_contract_float_number(self, amount_type):
        while True:
            if amount_type == "total_amount":
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
