import click

from src.database import SessionLocal

from src.controllers.main_controller import MainController


@click.group()
def client():
    pass

@client.command()
def create_client():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "create:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.client_controller.create_client_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="create", model_type="client")

@client.command()
def update_client():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "update:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.client_controller.update_client_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="update", model_type="client")


@client.command()
def delete_client():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "delete:client" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.user_controller.delete_model_with_view(session=session, model_type="client")

    else:
        main_controller.view.display_permission_denied(action="delete", model_type="client")

@client.command()
def filter_client():
    session = SessionLocal()
    main_controller = MainController()

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

@client.command()
def display_client():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    main_controller.user_controller.display_action(session=session, model_type="client")
