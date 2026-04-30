import click

from src.database import SessionLocal

from src.controllers.main_controller import MainController


@click.group()
def collaborator():
    pass

@collaborator.command()
@click.option('--role', prompt="▶ Which role do you want to create? (manager/commercial/technician)\n▶▶ ")
def create_collaborator(role):
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if user is None:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "create:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.create_collaborator_with_view(session=session, role=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="update", model_type=role)

@collaborator.command()
@click.option('--role', prompt="▶ Which collaborator role do you want to update? (manager/commercial/technician)\n▶▶ ")
def update_collaborator(role):
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "update:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.update_collaborator_with_view(session=session, role=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="update", model_type=role)

@collaborator.command()
@click.option('--role', prompt="▶ Which collaborator role do you want to delete? (manager/commercial/technician)\n▶▶ ")
def delete_collaborator(role):
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "update:collaborator" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.delete_model_with_view(session=session, model_type=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="delete", model_type=role)

@collaborator.command()
@click.option('--role', prompt="▶ Which model do you want to filter? (manager/commercial/technician)\n▶▶ ")
def filter_collaborator(role):
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "filter:manager" in permissions or "filter:commercial" in permissions or "filter:technician" in permissions:
        if role in main_controller.user_controller.COLLABORATORS.keys():
            main_controller.user_controller.filter_action_with_view(session=session, model_type=role)

        else:
            main_controller.view.display_wrong_collaborator_role()

    else:
        main_controller.view.display_permission_denied(action="filter", model_type=role)

@collaborator.command()
@click.option('--role', prompt="▶ Which model do you want to display? (manager/commercial/technician)\n▶▶ ")
def display_collaborator(role):
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if role in main_controller.user_controller.COLLABORATORS.keys():
        main_controller.user_controller.display_action(session=session, model_type=role)

    else:
        main_controller.view.display_wrong_collaborator_role()

@collaborator.command()
def logout():
    session = SessionLocal()

    main_controller = MainController()
    main_controller.user_controller.logout(session)
