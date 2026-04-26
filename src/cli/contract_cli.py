import click

from src.database import SessionLocal

from src.controllers.main_controller import MainController


@click.group()
def contract():
    pass

@contract.command()
def create_contract():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "create:contract" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.contract_controller.create_contract_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="create", model_type="contract")

@contract.command()
def update_contract():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "update:contract" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.contract_controller.update_contract_with_view(session=session)

    else:
        main_controller.view.display_permission_denied(action="update", model_type="contract")


@contract.command()
def delete_contract():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    if "delete:contract" in main_controller.user_controller.get_permissions(session=session, user=user):
        main_controller.user_controller.delete_model_with_view(session=session, model_type="contract")

    else:
        main_controller.view.display_permission_denied(action="update", model_type="contract")

@contract.command()
def filter_contract():
    session = SessionLocal()
    main_controller = MainController()

    user = main_controller.user_controller.get_current_user(session=session)
    if not user:
        main_controller.view.display_not_connected()
        return

    permissions = main_controller.user_controller.get_permissions(session=session, user=user)

    if "filter:contract" in permissions:
        main_controller.user_controller.filter_action_with_view(session=session, model_type="contract")

    else:
        main_controller.view.display_permission_denied(action="filter", model_type="contract")
