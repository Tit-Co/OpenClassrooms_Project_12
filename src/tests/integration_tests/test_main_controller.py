import sys
import unittest
from io import StringIO
from unittest.mock import Mock

from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.main_controller import MainController
from src.models.role import Role
from src.models.user import Manager


class TestMainController(unittest.TestCase):
    controller = MainController()

    credentials = {
        'email': 'admin@epicevents.url',
        'password': 'admin_pwd'
    }

    wrong_credentials = {
        'email': 'admin@admin.url',
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
        self.session = self.session_test()
        self.controller.init_db(self.db_engine, self.session)

    def tearDown(self) -> None:
        """
        Method called after every test case
        """
        self.session.close()

    def test_init_db_ok(self) -> None:
        """
        Test for checking the method that initializes the database
        """
        roles = self.session.query(Role).all()
        self.assertEqual(len(roles), 3)

        admin = self.session.query(Manager).first()
        self.assertNotEqual(admin, None)

    def test_run_with_wrong_input_raises_exception(self) -> None:
        """
        Test for checking if an exception is raises when a wrong input is given
        """
        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.controller.console = test_console
        self.controller.view.console = test_console

        self.controller.view.prompt_for_menu = Mock(return_value=3)

        with self.assertRaises(TypeError):
            self.controller.run(self.session)

        output = buffer.getvalue()

        self.assertIn("WELCOME TO EPIC EVENTS !", output)
        self.assertIn("▶ MAIN MENU ◀", output)
        self.assertIn("▷▷ 1. Log in", output)
        self.assertIn("▷▷ 2. Quit the app", output)

    def test_authenticate_ok(self) -> None:
        """
        Test for checking the method that authenticates a user in success case
        """
        email = self.credentials['email']
        password = self.credentials['password']

        answer = self.controller.authenticate(self.session, email, password)

        self.assertTrue(answer)

    def test_authenticate_fails(self) -> None:
        """
        Test for checking the method that authenticates a user in failure case
        """
        email = self.wrong_credentials['email']
        password = self.wrong_credentials['password']

        answer = self.controller.authenticate(self.session, email, password)

        self.assertFalse(answer)

    def test_init_permissions_ok(self) -> None:
        """
        Test for checking the method that initializes the user permissions
        """
        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.controller.view.console = test_console

        user = self.session.query(Manager).filter_by(is_active=True, email=self.credentials['email']).first()

        self.controller.init_permissions(self.session, user)

        output = buffer.getvalue()

        permissions = ["display:manager", "display:commercial", "display:technician",
                        "create:collaborator", "update:collaborator", "delete:collaborator",
                        "display:contract", "display:client", "display:event",
                        "create:contract", "update:contract", "delete:contract",
                        "update:event", "delete:event", "filter:event", "filter:client",
                        "filter:manager", "filter:commercial", "filter:technician"]

        self.assertEqual(self.controller.user_controller.permissions, permissions)
