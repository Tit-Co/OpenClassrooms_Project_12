import sys
import unittest
from io import StringIO
from unittest.mock import Mock

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

    def tearDown(self) -> None:
        """
        Method called after every test case
        """
        self.session.close()

    def test_init_db_ok(self) -> None:
        """
        Test for checking the method that initializes the database
        """
        self.controller.init_db(self.db_engine, self.session)

        roles = self.session.query(Role).all()
        self.assertEqual(len(roles), 3)

        admin = self.session.query(Manager).first()
        self.assertNotEqual(admin, None)

    def test_run_quit_case_ok(self) -> None:
        """
        Test for checking the method that quits the application
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.view.prompt_for_menu = Mock(return_value=2)

        with self.assertRaises(SystemExit):
            self.controller.run(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("WELCOME TO EPIC EVENTS !", output)
        self.assertIn("▶ MAIN MENU ◀", output)
        self.assertIn("▷▷ 1. Log in", output)
        self.assertIn("▷▷ 2. Quit the app", output)
        self.assertIn("👋  Goodbye ! 👋", output)

    def test_run_with_wrong_input_raises_exception(self) -> None:
        """
        Test for checking if an exception is raises when a wrong input is given
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.view.prompt_for_menu = Mock(return_value=3)

        with self.assertRaises(TypeError):
            self.controller.run(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("WELCOME TO EPIC EVENTS !", output)
        self.assertIn("▶ MAIN MENU ◀", output)
        self.assertIn("▷▷ 1. Log in", output)
        self.assertIn("▷▷ 2. Quit the app", output)

    def test_login_ok(self) -> None:
        """
        Test for checking the method that logs in a user in success case
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.init_db(self.db_engine, self.session)

        self.controller.view.prompt_for_continuing = Mock(return_value='anything_else')
        self.controller.view.prompt_for_email = Mock(return_value=self.credentials['email'])
        self.controller.view.prompt_for_password = Mock(return_value=self.credentials['password'])
        self.controller.check_password = Mock(return_value=True)

        self.controller.authenticate(self.session, self.credentials['email'], self.credentials['password'])

        self.controller.user_controller.collaborator_menu = Mock()

        self.controller.login(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("LOG IN", output)
        self.assertIn("You are going to enter the followings details", output)
        self.assertIn("Admin, you are successfully logged in", output)

    def test_authenticate_ok(self) -> None:
        """
        Test for checking the method that authenticates a user in success case
        """
        self.controller.init_db(self.db_engine, self.session)

        email = self.credentials['email']
        password = self.credentials['password']

        answer = self.controller.authenticate(self.session, email, password)

        self.assertTrue(answer)

    def test_authenticate_fails(self) -> None:
        """
        Test for checking the method that authenticates a user in failure case
        """
        self.controller.init_db(self.db_engine, self.session)

        email = self.wrong_credentials['email']
        password = self.wrong_credentials['password']

        answer = self.controller.authenticate(self.session, email, password)

        self.assertFalse(answer)

    def test_init_permissions_ok(self) -> None:
        """
        Test for checking the method that initializes the user permissions
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.init_db(self.db_engine, self.session)

        user = self.session.query(Manager).filter_by(email=self.credentials['email']).first()

        self.controller.init_permissions(self.session, user)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn(f"{user.name.capitalize()}, you are successfully logged in.", output)
