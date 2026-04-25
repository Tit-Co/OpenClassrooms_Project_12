import sys
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import Mock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.testing.pickleable import User

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.contract_controller import ContractController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.role import Role
from src.models.user import Commercial, Manager, Technician


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)
    contract_controller = ContractController(main_controller)

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

        manager = Manager(name="Manager Test",
                          email="manager@test.com",
                          password="test_pwd",
                          role_id=1
                          )
        self.session.add(admin)
        self.session.add(manager)
        self.session.commit()

        commercial = Commercial(name="Commercial name",
                                email="commercial.test@epicevents.url.com",
                                password="pwd_test",
                                role_id=2)

        self.session.add(commercial)
        self.session.commit()

        client = Client(name="Client Test",
                        email="client@clienttest.com",
                        phone="555123456",
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

        contract2 = Contract(client_id=client.id,
                            commercial_id=commercial.id,
                            total_amount=1000,
                            bill_to_pay=500,
                            creation_date=datetime.now(),
                            status=True)

        self.session.add(contract)
        self.session.add(contract2)
        self.session.commit()

        technician = Technician(
            name="Technician name",
            email="test@test.com",
            password="pwd_test",
            role_id=3
        )
        self.session.add(technician)
        self.session.commit()

        event = Event(name="Event Name",
                      start_date=datetime.now(),
                      end_date=datetime.now(),
                      location="Paris",
                      attendees=100,
                      notes="Notes",
                      contract_id=contract.id,
                      technician_id=technician.id,)

        self.session.add(event)
        self.session.commit()


        return {
            "managers": [admin, manager],
            "commercials": [commercial],
            "technicians": [technician],
            "clients": [client],
            "contracts": [contract, contract2],
            "events": [event]
        }

    def test_collaborator_menu_ok(self) -> None:
        """
        Test for checking the method that launches the collaborator menu
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(return_value=5)

        self.controller.action_submenu = Mock(side_effect=Exception("stop"))

        self.controller.collaborator_menu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR MENU ◀", output)

    def test_collaborator_menu_logout_ok(self) -> None:
        """
        Test for checking the method that logs out the collaborator
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(return_value=5)

        self.controller.collaborator_menu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR MENU ◀", output)
        self.assertIn("You are successfully logged out.", output)

    def test_collaborator_menu_contract_submenu_ok(self) -> None:
        """
        Test for checking the method that launches the contract submenu
        """
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

    def test_collaborator_submenu_ok(self) -> None:
        """
        Test for checking the method that launches the collaborator submenu
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(side_effect=[1, Exception("stop")])

        with self.assertRaises(Exception):
            self.controller.collaborator_submenu(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ EPIC EVENTS - COLLABORATOR SUBMENU ◀", output)

    def test_action_submenu_ok(self) -> None:
        """
        Test for checking the method that launches the action submenu
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.main_controller.view.prompt_for_menu = Mock(side_effect=[1, Exception("stop")])

        with self.assertRaises(Exception):
            self.controller.action_submenu(self.session, "contract", 6)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("▶ CONTRACT MENU ◀", output)

    def test_action_ok(self) -> None:
        """
        Test for checking the method action
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.get_models = Mock(return_value=[])
        self.controller.permissions = self.main_controller.role_permissions["MANAGER"]

        self.controller.action(self.session, "display", "contract")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You are going to display a contract.", output)
        self.assertIn("No contract to display.", output)

    def test_display_action_ok(self) -> None:
        """
        Test for checking the display action method
        """
        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.get_models = Mock(return_value=self.data)

        self.main_controller.view.prompt_for_model_id_with_action = Mock(return_value=1)

        self.controller.display_action(session=self.session, model_type="contract")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn(" • contracts - Here is the list : ", output)
        self.assertIn("Contract between the client", output)
        self.assertIn("Here is the contract : ", output)

    def test_create_action_ok(self) -> None:
        """
        Test for checking the create action method
        """
        with patch.object(
                self.main_controller.contract_controller,
                "create_contract_with_view"
        ) as mock_create:

            self.controller.create_action(session=self.session, model_type="contract")

            mock_create.assert_called_once_with(session=self.session)

    def test_create_collaborator_with_view_ok(self) -> None:
        """
        Test for checking the method that creates collaborator with view
        """
        with patch.object(
                self.main_controller.view,
                "prompt_for_collaborator"
        ) as mock_create:

            captured_output = StringIO()
            sys.stdout = captured_output

            mock_create.return_value = {"email": "test@test.com", "password": "password_test", "name": "name_test"}

            self.controller.create_collaborator_with_view(session=self.session, role="manager")

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("The manager has been successfully created.", output)

    def create_collaborator_ok(self) -> None:
        """
        Test for checking the method that creates collaborator in success case
        """
        data = {
            "email": "test@test.com",
            "password": "password",
            "name": "name",
            "role": "manager",
        }

        manager = Manager(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                role_id=self.session.query(Role).filter_by(name=data["role"].upper()).first().id)

        with patch.object(
            self.controller,
            "create_collaborator",
        ) as mock_create:

            collaborator = mock_create()
            self.assertEqual(collaborator, manager)

    def test_update_action_ok(self) -> None:
        """
        Test for checking the update action method in success case
        """
        with patch.object(
                self.main_controller.contract_controller,
                "update_contract_with_view"
        ) as mock_create:

            self.controller.update_action(session=self.session, model_type="contract")

            mock_create.assert_called_once_with(session=self.session)

    def test_update_action_technician_ok(self) -> None:
        """
        Test for checking the method that updates technician in success case
        """
        self.controller.get_models = Mock(return_value=self.data["technicians"])
        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)
        self.main_controller.view.prompt_for_collaborator = Mock(return_value=(
            "test@test.com",
            "pwd_test",
            "Technician name"))
        self.main_controller.view.prompt_for_collaborator_role = Mock(return_value=(2, "commercial"))

        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.update_action(session=self.session, model_type="technician")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("The collaborator (technician to commercial) "
                      "has been successfully updated.", output)

    def test_update_collaborator_ok(self) -> None:
        """
        Test for checking the method that updates collaborator in success case
        """
        new_data = {"name": "Commercial name",
                    "email": "commercial.test@epicevents.yahoo.com",
                    "password": "pwd_test_updated",
                    "role_id": 2}

        self.controller.update_collaborator(session=self.session, collaborator_id=1, data=new_data)

        updated_collaborator = self.session.query(Commercial).filter_by(is_active=True, id=1).first()

        self.assertEqual(updated_collaborator.name, new_data["name"])
        self.assertEqual(updated_collaborator.email, new_data["email"])
        self.assertEqual(updated_collaborator.password, new_data["password"])

    def test_change_role_for_collaborator_ok(self) -> None:
        """
        Test for checking the method that changes collaborator role in success case
        """
        new_data = {"name": "Commercial name",
                    "email": "commercial.test@epicevents.url",
                    "password": "pwd_test",
                    "role": "technician"}

        new_id = self.controller.change_role_for_collaborator(session=self.session,
                                                              collaborator_id=1,
                                                              current_role="commercial",
                                                              data=new_data)

        nb = len(self.session.query(Technician).filter_by(is_active=True).all())

        self.assertEqual(new_id, nb)

    def test_delete_action_for_contract_fails(self) -> None:
        """
        Test for checking the method that deletes a contract in failure case
        """
        self.main_controller.view.prompt_for_model_id = Mock(side_effect=[1])
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]

        self.controller.delete_action(session=self.session, model_type="contract")

        result = self.session.query(Contract).filter_by(is_active=True, id=1).first()

        self.assertIsNotNone(result)

    def test_delete_action_for_contract_ok(self) -> None:
        """
        Test for checking the method that deletes a contract in success case
        """
        self.main_controller.view.prompt_for_model_id = Mock(side_effect=[2])
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]

        self.controller.delete_action(session=self.session, model_type="contract")

        result = self.session.query(Contract).filter_by(is_active=True, id=2).first()

        self.assertIsNone(result)

    def test_delete_action_for_technician_ok(self) -> None:
        """
        Test for checking the method that deletes a technician in success case
        """
        self.main_controller.view.prompt_for_model_id = Mock(side_effect=[1])
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]

        self.controller.delete_action(session=self.session, model_type="technician")

        result = self.session.query(Technician).filter_by(is_active=True, id=1).first()

        self.assertIsNone(result)

    def test_delete_action_for_client_fails(self) -> None:
        """
        Test for checking the method that deletes a client in failure case
        """
        self.main_controller.view.prompt_for_model_id = Mock(side_effect=[1])
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["commercials"][0]

        self.controller.delete_action(session=self.session, model_type="client")

        result = self.session.query(Client).filter_by(is_active=True, id=1).first()

        self.assertIsNotNone(result)

    def test_delete_action_for_event_ok(self) -> None:
        """
        Test for checking the method that deletes an event in success case
        """
        self.main_controller.view.prompt_for_model_id = Mock(side_effect=[1])
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]

        self.controller.delete_action(session=self.session, model_type="event")

        result = self.session.query(Event).filter_by(is_active=True, id=1).first()

        self.assertIsNone(result)

    def test_delete_action_for_commercial_ok(self) -> None:
        """
        Test for checking the method that deletes a commercial in success case
        """
        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]

        self.controller.delete_action(session=self.session, model_type="commercial")

        result = self.session.query(Commercial).filter_by(is_active=True, id=1).first()

        self.assertIsNone(result)

    def test_update_collaborator_with_view_ok(self) -> None:
        """
        Test for checking the method that updates collaborator in success case
        """
        with patch.object(
                self.controller,
                "get_models"
        ) as mock_create:
            mock_create.return_value = self.data["technicians"]
            mock_create()

            self.main_controller.view.prompt_for_model_id = Mock(return_value=1)
            self.main_controller.view.prompt_for_collaborator = Mock(return_value=(
                "test@test.com",
                "pwd_test",
                "Technician name"))

            self.main_controller.view.prompt_for_collaborator_role = Mock(return_value=(2,"commercial"))

            captured_output = StringIO()
            sys.stdout = captured_output

            self.controller.update_collaborator_with_view(session=self.session, role="technician")

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("The collaborator (technician to commercial) "
                             "has been successfully updated.", output)

    def test_delete_technician_with_view_ok(self) -> None:
        """
        Test for checking the method that deletes a technician in success case
        """
        self.controller.get_models = Mock(return_value=self.data["technicians"])
        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)
        self.main_controller.view.prompt_for_confirmation = Mock(side_effect=['y'])

        self.controller.current_collaborator = self.data["managers"][1]


        captured_output = StringIO()
        sys.stdout = captured_output

        self.controller.delete_model_with_view(session=self.session, model_type="technician")

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("The technician has been successfully deleted.", output)


    def test_delete_collaborator_ok(self) -> None:
        """
        Test for checking the method that deletes a collaborator in success case
        """
        self.controller.delete_collaborator(session=self.session, collaborator_id=1, role="technician")

        self.controller.current_collaborator = self.data["managers"][1]

        result = self.session.query(Technician).filter_by(is_active=True, id=1).first()

        self.assertIsNone(result)

    def test_filter_action_ok(self) -> None:
        """
        Test for checking the filter action method
        """

        result = self.controller.filter_action(session=self.session,
                                               model_type="contract",
                                               my_filter="client_id",
                                               filter_value="1")

        self.assertEqual(result, self.data["contracts"])

    def test_filter_collaborator_ok(self) -> None:
        """
        Test for checking the method that creates collaborator with view
        """
        collaborator = self.controller.filter_collaborator(session=self.session,
                                                           model_type="manager",
                                                           my_filter="name",
                                                           filter_value="Manager Test",
                                                           class_name=Manager)

        self.assertEqual(collaborator, [self.data["managers"][1]])
