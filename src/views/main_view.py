import re


class MainView:
    @staticmethod
    def display_main_menu():
        print("WELCOME TO EPIC EVENTS !")
        print("▶ MAIN MENU ◀")
        print("▷▷ 1. Log in")
        print("▷▷ 2. Quit the app")

    @staticmethod
    def prompt_for_main_menu():
        while True:
            answer = input("▶ What do you want to do ? ")

            if not answer.isdigit():
                print("Please enter a number.")
                continue

            if answer not in ("1", "2"):
                print("Please choose between 1 and 2.")
                continue

            return int(answer)

    @staticmethod
    def display_goodbye():
        print("👋 Goodbye ! 👋")

    @staticmethod
    def display_logout():
        print("You are successfully logged out.")

    @staticmethod
    def prompt_for_continue():
        while True:
            input_key = input(" ▷▷ Type 'q' to go back or anything else to continue : ")
            return input_key.lower()

    @staticmethod
    def display_login_submenu():
        print("\n▶ LOG IN ◀\n")
        print("▷▷ You are going to enter the followings details :")
        print(" • your e-mail address")
        print(" • your password")

    @staticmethod
    def display_successfully_logged_in(name):
        print(f"{name.capitalize()}, you are successfully logged in.")

    @staticmethod
    def display_wrong_password():
        print("Invalid password.")

    @staticmethod
    def display_collaborator_does_not_exist():
        print("This collaborator does not exist.")

    @staticmethod
    def prompt_for_email():
        while True:
            email = input("▶ Enter the e-mail address : ")

            if not re.fullmatch(r'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', email):
                print("Invalid e-mail address.")
                continue

            return email

    @staticmethod
    def prompt_for_password():
        return input("▶ Enter the password : ")
