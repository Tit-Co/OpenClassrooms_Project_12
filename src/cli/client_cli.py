import click

from click_aliases import ClickAliasedGroup
from src.controllers.main_controller import MainController
from src.database import DATABASE_URL, get_engine, get_session


@click.group(cls=ClickAliasedGroup)
@click.pass_context
def client(ctx):
    ctx.ensure_object(dict)


@client.command(aliases=['create'])
@click.pass_context
def create_client(ctx):
    ctx.ensure_object(dict)
    db_engine = ctx.obj.get("db_engine") or get_engine(database_url=DATABASE_URL)
    session = ctx.obj.get("session") or get_session(db_engine)()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "create:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.client_controller.create_client_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="create", model_type="client")


@client.command(aliases=['update'])
@click.pass_context
def update_client(ctx):
    ctx.ensure_object(dict)
    db_engine = ctx.obj.get("db_engine") or get_engine(database_url=DATABASE_URL)
    session = ctx.obj.get("session") or get_session(db_engine)()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "update:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.client_controller.update_client_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="update", model_type="client")


@client.command(aliases=['delete'])
@click.pass_context
def delete_client(ctx):
    ctx.ensure_object(dict)
    db_engine = ctx.obj.get("db_engine") or get_engine(database_url=DATABASE_URL)
    session = ctx.obj.get("session") or get_session(db_engine)()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "delete:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.user_controller.delete_model_with_view(session=session, model_type="client")

    else:
        main_controller.view.display_permission_denied(action="delete", model_type="client")


@client.command(aliases=['filter'])
@click.pass_context
def filter_client(ctx):
    ctx.ensure_object(dict)
    db_engine = ctx.obj.get("db_engine") or get_engine(database_url=DATABASE_URL)
    session = ctx.obj.get("session") or get_session(db_engine)()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "filter:client" in permissions:
        main_controller.view.display_action_introduction(action="filter",
                                                         model_type="client")
        main_controller.user_controller.filter_action_with_view(session=session, model_type="client")

    else:
        main_controller.view.display_permission_denied(action="filter", model_type="client")


@client.command(aliases=['display'])
@click.pass_context
def display_client(ctx):
    ctx.ensure_object(dict)
    db_engine = ctx.obj.get("db_engine") or get_engine(database_url=DATABASE_URL)
    session = ctx.obj.get("session") or get_session(db_engine)()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    main_controller.user_controller.display_action(session=session, model_type="client")
