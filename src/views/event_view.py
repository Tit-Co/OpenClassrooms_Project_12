class EventView:
    def __init__(self, main_view):
        self.main_view = main_view

    def display_event(self, event, add_on):
        self.main_view.display_title(model_type="event")
        print(f"Id : {event.id}")
        print(f"Contract id : {event.contract_id}")
        print(f"Client name : {add_on.get("client_name") or ""}")
        print(f"Client phone : {add_on.get("client_phone") or ""}")
        print(f"Client e-mail : {add_on.get("client_email") or ""}")
        print(f"Start date : {event.start_date if event.start_date else ""}")
        print(f"End date : {event.end_date if event.end_date else ""}")
        print(f"Technician name : {add_on.get("technician_name") or ""}")
        print(f"Location : {event.location if event.location else ""}")
        print(f"Attendees : {event.attendees if event.attendees else ""}")
        print(f"Notes : {event.notes if event.notes else ""}")

    def prompt_for_event(self, contracts, technicians):
        self.main_view.display_models(model_type="contract", models=contracts)
        contract_id = self.prompt_for_id(model_type="contract")

        self.main_view.display_models(model_type="technician", models=technicians)
        technician_id = self.prompt_for_id(model_type="technician")

        name = self.main_view.prompt_for_string(model_type="event", field="name")

        start_date = self.main_view.prompt_for_date(model_type="event", field="start date")

        end_date = self.main_view.prompt_for_date(model_type="event", field="end date")

        location = self.main_view.prompt_for_string_if_known(model_type="event", field="location")

        attendees = self.prompt_for_integer()

        notes = self.main_view.prompt_for_string_if_known(model_type="event", field="notes")

        return name, contract_id, start_date, end_date, technician_id, location, attendees, notes

    @staticmethod
    def prompt_for_id(model_type):
        while True:
            answer = input(f"\n▶ Please select a {model_type} for the event if possible:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter a number or leave blank to continue.")

    @staticmethod
    def prompt_for_integer():
        while True:
            answer = input(f"\n▶ Please enter the number of attendees if known:\n▶▶ ").strip()

            if answer.isdigit() or answer == "":
                return int(answer) if answer else None

            print("Please enter an integer or leave blank to continue.")
