import click

from src.controllers.main_controller import MainController
from src.database import get_session, get_engine, DATABASE_URL


@click.group()
@click.pass_context
def collaborator(ctx):
    ctx.ensure_object(dict)

@collaborator.command()
@click.pass_context
def create_collaborator(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if user is None:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    role = main_controller.view.prompt_for_collaborator_role_to_action(action="create")

    if "create:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.create_collaborator_with_view(session=session, role=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="update", model_type=role)

@collaborator.command()
@click.pass_context
def update_collaborator(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    role = main_controller.view.prompt_for_collaborator_role_to_action(action="update")

    if "update:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.update_collaborator_with_view(session=session, role=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="update", model_type=role)

@collaborator.command()
@click.pass_context
def delete_collaborator(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    role = main_controller.view.prompt_for_collaborator_role_to_action(action="delete")

    if "update:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.delete_model_with_view(session=session, model_type=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="delete", model_type=role)

@collaborator.command()
@click.pass_context
def filter_collaborator(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    role = main_controller.view.prompt_for_collaborator_role_to_action(action="filter")

    if "filter:manager" in permissions or "filter:commercial" in permissions or "filter:technician" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.filter_action_with_view(session=session, model_type=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="filter", model_type=role)

@collaborator.command()
@click.pass_context
def display_collaborator(ctx, role):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    role = main_controller.view.prompt_for_collaborator_role_to_action(action="display")

    if role in main_controller.user_controller.COLLABORATORS.keys():
        main_controller.user_controller.display_action(session=session, model_type=role)

    else:
        main_controller.view.display_wrong_collaborator_role()

@collaborator.command()
@click.pass_context
def logout(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or get_session(get_engine(database_url=DATABASE_URL))
    main_controller = ctx.obj.get("main_controller") or MainController()

    main_controller.user_controller.logout(session)
