import unittest
from io import StringIO
from unittest.mock import Mock

from click.testing import CliRunner
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cli.collaborator_cli import collaborator
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.role import Role
from src.models.user import Commercial, Manager


class TestCollaboratorCLI(unittest.TestCase):
    main_controller = MainController()

    credentials = {
        'email': 'admin@epicevents.url',
        'password': 'admin_pwd'
    }

    @classmethod
    def setUpClass(cls) -> None:
        """
        Method called once before all test cases
        """
        cls.db_engine = create_engine("sqlite:///:memory:")
        cls.session_test = sessionmaker(bind=cls.db_engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Method called once after all test cases
        """
        cls.db_engine.dispose()

    def setUp(self) -> None:
        """
        Method called before every test case
        """
        Base.metadata.drop_all(bind=self.db_engine)
        Base.metadata.create_all(bind=self.db_engine)
        self.session = self.session_test()
        self.data = self.seed_data()

    def tearDown(self) -> None:
        """
        Method called after every test case
        """
        self.session.close()

    def seed_data(self) -> dict:
        """
        Method to seed data
        Returns:
        A dictionary with seed data
        """
        role_manager = Role(
            name="MANAGER",
        )
        role_commercial = Role(
            name="COMMERCIAL",
        )
        role_technician = Role(
            name="TECHNICIAN",
        )
        self.session.add(role_manager)
        self.session.add(role_commercial)
        self.session.add(role_technician)
        self.session.commit()

        admin_credentials = {
            "name": "admin",
            "email": "admin@epicevents.url",
            "password": "admin_pwd",
            "role": "MANAGER"
        }

        admin = Manager(name=admin_credentials["name"],
                        email=admin_credentials["email"],
                        password=admin_credentials["password"],
                        role_id=1
                        )
        self.session.add(admin)
        self.session.commit()

        commercial = Commercial(name="Commercial name",
                                email="commercial.test@epicevents.url.com",
                                password="pwd_test",
                                role_id=2)

        self.session.add(commercial)
        self.session.commit()

        return {
            "managers": [admin],
            "commercials": [commercial]
        }

    def test_update_collaborator_in_same_role_ok(self):
        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        user = self.data.get("managers")[0]

        permissions = self.main_controller.role_permissions["MANAGER"]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.user_controller.get_permissions = Mock(return_value=permissions)
        test_controller.view.prompt_for_collaborator_role_to_action = Mock(return_value="commercial")
        test_controller.view.prompt_for_model_id = Mock(return_value=1)
        test_controller.view.prompt_for_collaborator = Mock(return_value=("new.commercial.test@epicevents.url",
                                                                          "pwd_test",
                                                                          "Commercial New Name"))
        test_controller.view.prompt_for_collaborator_role = Mock(return_value=(2, "commercial"))

        runner.invoke(collaborator,
                      ["update-collaborator"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()
        self.assertIn("⯀ COMMERCIALS TO DISPLAY", output)
        self.assertIn(f"Name : {self.data["commercials"][0].name}", output)
        self.assertIn(f"E-mail : {self.data["commercials"][0].email}", output)
        self.assertIn(f"▶ Please enter the new data for the commercial "
                      f"n°{self.data["commercials"][0].id}.", output)
        self.assertIn("✅ The collaborator has been successfully updated.", output)

        commercial = self.session.query(Commercial).filter(Commercial.name == "Commercial New Name").first()
        self.assertEqual(commercial.role_id, 2)

        self.assertIn(f"Name : Commercial New Name", output)
        self.assertIn(f"E-mail : new.commercial.test@epicevents.url", output)

    def test_update_collaborator_in_another_role_ok(self):
        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        user = self.data.get("managers")[0]

        permissions = self.main_controller.role_permissions["MANAGER"]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console


        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.user_controller.get_permissions = Mock(return_value=permissions)
        test_controller.view.prompt_for_collaborator_role_to_action = Mock(return_value="commercial")
        test_controller.view.prompt_for_model_id = Mock(return_value=1)
        test_controller.view.prompt_for_collaborator = Mock(return_value=("new.manager.test@epicevents.url",
                                                                          "pwd_test",
                                                                          "Manager New Name"))
        test_controller.view.prompt_for_collaborator_role = Mock(return_value=(1, "manager"))

        runner.invoke(collaborator,
                      ["update-collaborator"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()
        self.assertIn("⯀ COMMERCIALS TO DISPLAY", output)
        self.assertIn(f"Name : {self.data["commercials"][0].name}", output)
        self.assertIn(f"E-mail : {self.data["commercials"][0].email}", output)
        self.assertIn(f"▶ Please enter the new data for the commercial "
                      f"n°{self.data["commercials"][0].id}.", output)
        self.assertIn("✅ The collaborator (commercial to manager) has been successfully updated.", output)

        manager = self.session.query(Manager).filter(Manager.name == "Manager New Name").first()
        self.assertEqual(manager.role_id, 1)

        self.assertIn(f"Name : Manager New Name", output)
        self.assertIn(f"E-mail : new.manager.test@epicevents.url", output)
        self.assertIn(f"Role : manager", output)

    def test_delete_collaborator_ok(self):
        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        user = self.data.get("managers")[0]

        permissions = self.main_controller.role_permissions["MANAGER"]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.console = test_console
        self.main_controller.view.console = test_console

        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.user_controller.get_permissions = Mock(return_value=permissions)
        test_controller.view.prompt_for_collaborator_role_to_action = Mock(return_value="commercial")
        test_controller.view.prompt_for_model_id = Mock(return_value=1)
        test_controller.view.prompt_for_confirmation = Mock(return_value="y")

        commercials = test_session.query(Commercial).filter(Commercial.is_active == True).all()
        self.assertEqual(len(commercials), len(self.data["commercials"]))

        runner.invoke(collaborator,
                      ["delete-collaborator"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()

        commercials = test_session.query(Commercial).filter(Commercial.is_active == True).all()
        self.assertEqual(len(commercials), len(self.data["commercials"]) - 1)
        self.assertIn("⯀ COMMERCIALS TO DISPLAY", output)
        commercial_deleted = (
            test_session.query(Commercial)
            .filter(Commercial.name == self.data["commercials"][0].name)
            .first()
            )
        self.assertFalse(commercial_deleted.is_active)
        self.assertIn("✅ The commercial has been successfully deleted.", output)
