import click

from src.database import SessionLocal

from src.cli.collaborator_cli import collaborator
from src.cli.contract_cli import contract
from src.cli.client_cli import client
from src.cli.event_cli import event

from src.controllers.main_controller import MainController


@click.group()
def cli():
    pass

cli.add_command(collaborator)
cli.add_command(contract)
cli.add_command(client)
cli.add_command(event)

@cli.command()
def login():
    session = SessionLocal()

    main_controller = MainController()

    email = main_controller.view.prompt_for_email()

    password = main_controller.view.prompt_for_password()

    # if main_controller.login(session=session, email=email, password=password):
    #     user = main_controller.user_controller.get_collaborator_by_mail(session=session, email=email)
    #     main_controller.view.display_successfully_logged_in(user.name)
    #
    # elif not main_controller.login(session=session, email=email, password=password):
    #     main_controller.view.display_credentials_wrong()
    #
    # else:
    #     main_controller.view.display_something_wrong("logging")
    result = main_controller.login(session=session, email=email, password=password)
    if result:
        user = main_controller.user_controller.get_collaborator_by_mail(session=session, email=email)
        main_controller.view.display_successfully_logged_in(name=user.name)

    elif result is None:
        main_controller.view.display_collaborator_not_exists()

    else:
        main_controller.view.display_wrong_password()

    session.close()


if __name__ == "__main__":
    cli()
