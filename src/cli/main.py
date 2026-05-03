import click

from src.database import SessionLocal

from src.cli.collaborator_cli import collaborator
from src.cli.contract_cli import contract
from src.cli.client_cli import client
from src.cli.event_cli import event

from src.controllers.main_controller import MainController


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
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()
    db_engine = ctx.obj.get("db_engine")

    if not email:
        email = main_controller.view.prompt_for_email()

    if not password:
        password = main_controller.view.prompt_for_password()

    result = main_controller.login(session=session, email=email, password=password)

    session.close()


if __name__ == "__main__":
    cli()
