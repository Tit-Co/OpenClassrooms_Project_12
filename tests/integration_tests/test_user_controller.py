import sys
import unittest

from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.main_controller import MainController


class TestMainController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)

    credentials = {
        'email': 'admin@epicevents.url',
        'password': 'admin_pwd'
    }

    wrong_credentials = {
        'email': 'admin@admin.url',
        'password': 'admin_pwd'
    }

    @classmethod
    def setUpClass(cls):
        cls.db_engine = create_engine("sqlite:///:memory:")
        cls.session_test = sessionmaker(bind=cls.db_engine)

    @classmethod
    def tearDownClass(cls):
        cls.db_engine.dispose()

    def setUp(self):
        self.session = self.session_test()

    def tearDown(self):
        self.session.close()

    def test_collaborator_menu_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(return_value=5)

        self.controller.action_submenu = Mock(side_effect=Exception("stop"))

        self.controller.collaborator_menu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR MENU ◀", output)

    def test_collaborator_menu_logout_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(return_value=5)

        self.controller.collaborator_menu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR MENU ◀", output)
        self.assertIn("You are successfully logged out.", output)

    def test_collaborator_menu_contract_submenu_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(side_effect=[2, Exception("stop")])

        self.controller.action = Mock(side_effect=Exception("stop"))

        with self.assertRaises(Exception):
            self.controller.collaborator_menu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR MENU ◀", output)
        self.assertIn("▶ CONTRACT MENU ◀", output)
        self.assertIn("▷▷ 1. Display", output)
        self.assertIn("▷▷ 2. Create", output)
        self.assertIn("▷▷ 3. Update", output)
        self.assertIn("▷▷ 4. Delete", output)
        self.assertIn("▷▷ 5. Filter", output)
        self.assertIn("▷▷ 6. Go back", output)

    def test_collaborator_submenu_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(side_effect=[1, Exception("stop")])

        with self.assertRaises(Exception):
            self.controller.collaborator_submenu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀", output)

    def test_action_submenu_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(side_effect=[1, Exception("stop")])

        with self.assertRaises(Exception):
            self.controller.action_submenu(self.session, "contract", 6)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ CONTRACT MENU ◀", output)

    def test_action_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.get_models = Mock(return_value=[])
        self.controller.permissions = self.main_controller.role_permissions["MANAGER"]

        self.controller.action(self.session, "display", "contract")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You are going to display a contract.", output)
        self.assertIn("No contract to display.", output)
