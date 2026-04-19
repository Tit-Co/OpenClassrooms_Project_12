import sys
import unittest

from datetime import datetime
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.user import Commercial, Technician


class TestCollaboratorController(unittest.TestCase):
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
        Base.metadata.drop_all(bind=self.db_engine)
        Base.metadata.create_all(bind=self.db_engine)
        self.session = self.session_test()
        self.data = self.seed_data()

    def tearDown(self):
        self.session.close()

    def seed_data(self):
        commercial = Commercial(name="Commercial name",
                                email="commercial.test@epicevents.url.com",
                                password="pwd_test",
                                role_id=2)

        self.session.add(commercial)
        self.session.commit()

        client = Client(name="Client Test",
                        email="client@clienttest.com",
                        phone=555123456,
                        company="Company Test",
                        creation_date=datetime.now(),
                        last_update=datetime.now(),
                        commercial_id=commercial.id)

        self.session.add(client)
        self.session.commit()

        contract = Contract(client_id=client.id,
                            commercial_id=commercial.id,
                            total_amount=100,
                            bill_to_pay=50,
                            creation_date=datetime.now(),
                            status=True)

        self.session.add(contract)
        self.session.commit()

        return {
            "commercial": commercial,
            "client": client,
            "contract": contract
        }

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

    def test_display_action_ok(self):
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.get_models = Mock(return_value=[self.data["contract"]])
        self.main_controller.view.prompt_for_model_id_with_action = Mock(return_value=1)

        self.controller.display_action(session=self.session, model_type="contract")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn(" • contracts - Here is the list : ", output)
        self.assertIn("Contract n° ", output)
        self.assertIn("Here is the contract : ", output)
