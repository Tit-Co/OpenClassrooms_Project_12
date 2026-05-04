import click

from src.cli.client_cli import client
from src.cli.collaborator_cli import collaborator
from src.cli.contract_cli import contract
from src.cli.event_cli import event
from src.controllers.main_controller import MainController
from src.database import get_session, get_engine, DATABASE_URL


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

cli.add_command(collaborator)
cli.add_command(contract)
cli.add_command(client)
cli.add_command(event)

@cli.command()
@click.option("--email", required=False)
@click.option("--password", required=False)
@click.pass_context
def login(ctx, email, password):
    ctx.ensure_object(dict)

    db_engine = ctx.obj["db_engine"] or get_engine(database_url=DATABASE_URL)
    session = ctx.obj["session"] or get_session(db_engine)()
    main_controller = ctx.obj["main_controller"] or MainController()

    main_controller.init_db(db_engine, session)

    if not email:
        email = main_controller.view.prompt_for_email()

    if not password:
        password = main_controller.view.prompt_for_password()

    try:
        result = main_controller.authenticate(session=session,
                                              email=email,
                                              password=password)
    except Exception as e:
        main_controller.view.display_error_while_logging_in()

    session.close()


if __name__ == "__main__":
    cli()
