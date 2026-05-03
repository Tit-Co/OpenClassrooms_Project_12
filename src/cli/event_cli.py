import click

from src.database import SessionLocal

from src.controllers.main_controller import MainController


@click.group()
@click.pass_context
def event(ctx):
    ctx.ensure_object(dict)

@event.command()
@click.pass_context
def create_event(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "create:event" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.event_controller.create_event_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="create", model_type="event")

@event.command()
@click.pass_context
def update_event(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "update:event" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.event_controller.update_event_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="update", model_type="event")


@event.command()
@click.pass_context
def delete_event(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "delete:event" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.user_controller.delete_model_with_view(session=session, model_type="event")

    else:
        main_controller.view.display_permission_denied(action="delete", model_type="event")

@event.command()
@click.pass_context
def filter_event(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "filter:event" in permissions:
        main_controller.view.display_action_introduction(action="filter",
                                                         model_type="event")
        main_controller.user_controller.filter_action_with_view(session=session, model_type="event")

    else:
        main_controller.view.display_permission_denied(action="filter", model_type="event")

@event.command()
@click.pass_context
def display_event(ctx):
    ctx.ensure_object(dict)
    session = ctx.obj.get("session") or SessionLocal()
    main_controller = ctx.obj.get("main_controller") or MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    main_controller.user_controller.display_action(session=session, model_type="event")
