import sys
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.event_controller import EventController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.role import Role
from src.models.user import Commercial, Technician, Manager


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)
    event_controller = EventController(main_controller)


    @classmethod
    def setUpClass(cls) -> None:
        """
        Method called once before all test cases.
        """
        cls.db_engine = create_engine("sqlite:///:memory:")
        cls.session_test = sessionmaker(bind=cls.db_engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Method called once after all test cases.
        """
        cls.db_engine.dispose()

    def setUp(self) -> None:
        """
        Method called before each test case.
        """
        Base.metadata.drop_all(bind=self.db_engine)
        Base.metadata.create_all(bind=self.db_engine)
        self.session = self.session_test()
        self.data = self.seed_data()

    def tearDown(self) -> None:
        """
        Method called after each test case.
        """
        self.session.close()

    def seed_data(self) -> dict:
        """
        Method to seed data for testing.
        Returns:

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

        manager = Manager(name=admin_credentials["name"],
                          email=admin_credentials["email"],
                          password=admin_credentials["password"],
                          role_id=1
                          )
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

        contract_2 = Contract(client_id=client.id,
                             commercial_id=commercial.id,
                             total_amount=1000,
                             bill_to_pay=500,
                             creation_date=datetime.now(),
                             status=True)

        self.session.add(contract)
        self.session.add(contract_2)
        self.session.commit()

        technician = Technician(
            name="Technician name",
            email="test@test.com",
            password="pwd_test",
            role_id=3
        )
        self.session.add(technician)
        self.session.commit()

        event = Event(name="Event Test",
                      start_date=datetime.now(),
                      end_date=datetime.now(),
                      location="Paris",
                      attendees=100,
                      notes="Notes",
                      contract_id=contract.id,
                      technician_id=technician.id)

        event_2 = Event(name="Event Test 2",
                      start_date=datetime.now(),
                      end_date=datetime.now(),
                      location="Madrid",
                      attendees=1000,
                      notes="Notes",
                      technician_id=technician.id)

        self.session.add(event)
        self.session.add(event_2)
        self.session.commit()

        return {
            "managers": [manager],
            "commercials": [commercial],
            "technicians": [technician],
            "clients": [client],
            "contracts": [contract, contract_2],
            "events": [event, event_2]
        }

    def test_create_event_with_view_ok(self) -> None:
        """
        Test for checking the method that creates an event with view in success case
        """
        def mock_get_models(session, model_type):
            if model_type == "technician":
                return self.data["technicians"]
            elif model_type == "contract":
                return self.data["contracts"]
            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.event_view.prompt_for_event = Mock(return_value=[
            "Event Name",
            1,
            datetime.now(),
            datetime.now(),
            1,
            "Paris",
            175,
            "Notes"
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.event_controller.create_event_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("The event has been successfully created.", output)

    def test_create_event_with_view_returns_already_exists(self) -> None:
        """
        Test for checking the method that creates an event with view in success case
        Returns:

        """
        def mock_get_models(session, model_type):
            if model_type == "technician":
                return self.data["technicians"]
            elif model_type == "contract":
                return self.data["contracts"]
            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.event_view.prompt_for_event = Mock(return_value=[
            "Event Test",
            1,
            datetime.now(),
            datetime.now(),
            1,
            "Paris",
            175,
            "Notes"
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.event_controller.create_event_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("❌ This event already exists.", output)

    def test_create_event_ok(self) -> None:
        """
        Test for checking the method that creates an event in success case
        """
        data = {
            "name": "Event Name Test",
            "contract_id": 1,
            "start_date": datetime.now(),
            "end_date": datetime.now(),
            "technician_id": 1,
            "location": "Paris",
            "notes": "Notes",
            "attendees": 100,
        }

        self.event_controller.create_event(self.session, data)
        event = self.session.query(Event).filter_by(is_active=True, name="Event Name Test").first()

        self.assertEqual(event.id, 3)

    def test_update_event_with_view_ok(self) -> None:
        """
        Test for checking the method that updates an event with view in success case
        Returns:

        """
        def mock_get_models(session, model_type):
            if model_type == "technician":
                return self.data["technicians"]

            elif model_type == "contract":
                return self.data["contracts"]

            elif model_type == "event":
                return self.data["events"]

            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)

        self.main_controller.view.event_view.prompt_for_event = Mock(return_value=[
            "Event Updated",
            1,
            datetime.now(),
            datetime.now(),
            1,
            "New York City",
            200,
            "Notes Updated"
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.event_controller.update_event_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        event = self.session.query(Event).filter_by(is_active=True, id=1).first()

        self.assertIn("The event has been successfully updated.", output)
        self.assertEqual(event.name, "Event Updated")
        self.assertEqual(event.location, "New York City")
        self.assertEqual(event.attendees, 200)
        self.assertEqual(event.notes, "Notes Updated")

    def test_update_event_ok(self) -> None:
        """
        Test for checking the method that updates an event in success case
        """
        new_data = {
            "name": "Event Name Test",
            "contract_id": 1,
            "start_date": datetime.now(),
            "end_date": datetime.now(),
            "technician_id": 1,
            "location": "London",
            "notes": "Notes",
            "attendees": 100,
        }

        self.event_controller.update_event(session=self.session, event_id=1, data=new_data)
        client = self.session.query(Event).filter_by(is_active=True, id=1).first()

        self.assertEqual(client.location, "London")

    def test_delete_event_ok(self) -> None:
        """
        Test for checking the method that deletes an event in success case
        """
        self.event_controller.delete_event(session=self.session, event_id=2)

        event = self.session.query(Event).filter_by(is_active=True, id=2).first()

        self.assertIsNone(event)
