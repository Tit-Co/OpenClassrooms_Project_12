import sys
import unittest
from datetime import datetime
from io import StringIO

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.client_controller import ClientController
from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.event_controller import EventController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Commercial, Technician, Manager


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    client_controller = ClientController(main_controller)
    controller = CollaboratorController(main_controller)
    event_controller = EventController(main_controller)

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

        self.session.add(contract)
        self.session.commit()

        return {
            "manager": admin,
            "commercial": commercial,
            "client": client,
            "contract": contract
        }

    def test_get_models_contracts(self) -> None:
        """
        Test for checking the method that gets contracts
        """
        models = self.controller.get_models(self.session, "contract")

        self.assertEqual(len(models),3)
        self.assertEqual(models.get("contracts")[0].id, self.data["contract"].id)
        self.assertEqual(models.get("contracts")[0].client_id, self.data["client"].id)
        self.assertEqual(models.get("contracts")[0].commercial_id, self.data["commercial"].id)
        self.assertEqual(models.get("contracts")[0].total_amount, 100)
        self.assertEqual(models.get("contracts")[0].bill_to_pay, 50)
        self.assertEqual(models.get("contracts")[0].status, True)

    def test_get_models_clients(self) -> None:
        """
        Test for checking the method that gets clients
        """
        clients = self.controller.get_models(self.session, "client")

        self.assertEqual(len(clients),1)
        self.assertEqual(clients[0].id, self.data["client"].id)
        self.assertEqual(clients[0].name, self.data["client"].name)
        self.assertEqual(clients[0].email, self.data["client"].email)
        self.assertEqual(clients[0].phone, self.data["client"].phone)
        self.assertEqual(clients[0].company, self.data["client"].company)
        self.assertEqual(clients[0].creation_date, self.data["client"].creation_date)
        self.assertEqual(clients[0].last_update, self.data["client"].last_update)
        self.assertEqual(clients[0].commercial_id, self.data["client"].commercial_id)

    def test_get_model(self) -> None:
        """
        Test for checking the method that gets model
        """
        model = self.controller.get_model(self.session, "contract", self.data["contract"].id)

        self.assertEqual(model.id, self.data["contract"].id)
        self.assertEqual(model.client_id, self.data["client"].id)
        self.assertEqual(model.commercial_id, self.data["commercial"].id)
        self.assertEqual(model.total_amount, 100)
        self.assertEqual(model.bill_to_pay, 50)
        self.assertEqual(model.status, True)

    def test_get_client(self) -> None:
        """
        Test for checking the method that gets client
        """
        model = self.main_controller.client_controller.get_client(self.session, self.data["client"].id)

        self.assertEqual(model.id, self.data["client"].id)
        self.assertEqual(model.name, "Client Test")
        self.assertEqual(model.email, "client@clienttest.com")
        self.assertEqual(model.phone, "555123456")
        self.assertEqual(model.company, "Company Test")
        self.assertEqual(model.commercial_id, 1)

    def test_get_event(self) -> None:
        """
        Test for checking the method that gets event
        """
        technician = Technician(name="Technician name",
                               email="technician.test@epicevents.url.com",
                               password="pwd_test_2",
                               role_id=3)
        self.session.add(technician)
        self.session.commit()

        event = Event(name="Event Test",
                          start_date=datetime.now(),
                          end_date=datetime.now(),
                          location="Location Test",
                          attendees=100,
                          notes="Notes event",
                          contract_id=self.data["contract"].id,
                          technician_id=technician.id)
        self.session.add(event)
        self.session.commit()

        model = self.main_controller.event_controller.get_event(self.session, event.id)

        self.assertEqual(model.id, event.id)
        self.assertEqual(model.name, "Event Test")
        self.assertEqual(model.location, "Location Test")
        self.assertEqual(model.attendees, 100)
        self.assertEqual(model.contract_id, self.data["contract"].id)
        self.assertEqual(model.technician_id, technician.id)

    def test_logout(self) -> None:
        """
        Test for checking the logout method
        """
        captured_output = StringIO()
        sys.stdout = captured_output


        self.controller.logout(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You are successfully logged out.", output)

    def test_get_collaborator_by_id(self) -> None:
        """
        Test for checking the method that gets collaborator by its id
        """
        collaborator = self.controller.get_collaborator_by_id(session=self.session,
                                                              collaborator_id=self.data["commercial"].id,
                                                              role="commercial")

        self.assertEqual(collaborator.id, self.data["commercial"].id)

    def test_get_collaborator_by_email(self) -> None:
        """
        Test for checking the method that gets collaborator by its email
        """
        collaborator = self.controller.get_collaborator_by_mail(session=self.session,
                                                                email=self.data["commercial"].email)

        self.assertEqual(collaborator.email, self.data["commercial"].email)

    def test_exists_returns_true(self) -> None:
        """
        Test for checking the method that tests if a model already exists in true case
        """
        result = self.controller.model_exists(session=self.session,
                                              model_type="client",
                                              value="client@clienttest.com")

        self.assertTrue(result)

    def test_exists_returns_false(self) -> None:
        """
        Test for checking the method that tests if a model already exists in false case
        """
        result = self.controller.model_exists(session=self.session,
                                              model_type="client",
                                              value="unautreemail@clienttest.com")

        self.assertFalse(result)

    def test_goodbye(self) -> None:
        """
        Test for checking the exit method
        """
        with self.assertRaises(SystemExit) as mock:
            captured_output = StringIO()
            sys.stdout = captured_output

            self.main_controller.goodbye()

            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()

            self.assertIn("Goodbye !", output)
            self.assertEqual(mock.exception.code, 1)

    def test_is_float_ok(self) -> None:
        """
        Test for checking the is_float method in a True case
        """
        float = self.controller.is_float(s="152.23")

        self.assertTrue(float)

    def test_is_float_return_false_with_str(self) -> None:
        """
        Test for checking the is_float method in a false case
        """
        float = self.controller.is_float(s="test")

        self.assertFalse(float)

    def test_is_date_ok(self) -> None:
        """
        Test for checking the is_date method in a success case
        """
        date = self.controller.is_date(s="25/04/26 11:00")

        self.assertTrue(date)

    def test_is_date_return_false_with_wrong_format(self) -> None:
        """
        Test for checking the is_date method in a failure case
        """
        date = self.controller.is_date(s="25/04/26 11")

        self.assertFalse(date)

    def test_is_bool(self) -> None:
        """
        Test for checking the is_bool method in a success case
        """
        my_bool = self.controller.is_bool(s="true")

        self.assertTrue(my_bool)

    def test_is_bool_fails(self) -> None:
        """
        Test for checking the is_bool method in a failure case
        """
        my_bool = self.controller.is_bool(s="test")

        self.assertIsNone(my_bool)

    def test_get_object(self) -> None:
        """
        Test for checking the get object method
        """
        my_object = self.controller.get_object_by_id(session=self.session, model_type="client", object_id=1)

        self.assertEqual(my_object, self.data["client"])

    def test_get_admin_ok(self) -> None:
        """
        Test for checking the get admin method
        """
        admin = self.controller.get_admin(session=self.session)

        self.assertEqual(admin, self.data["manager"])

    def test_filter_value_str_ok(self):
        filter_value = self.controller.process_filter_value("test", filter_value="test")
        self.assertEqual(filter_value, "test")

    def test_filter_value_int_ok(self):
        filter_value = self.controller.process_filter_value("test", filter_value="2")
        self.assertEqual(filter_value, 2)

    def test_filter_value_float_ok(self):
        filter_value = self.controller.process_filter_value("test", filter_value="12.23")
        self.assertEqual(filter_value, 12.23)

    def test_filter_value_date_ok(self):
        filter_value = self.controller.process_filter_value("", filter_value="26/04/26 11:00")
        self.assertEqual(filter_value, datetime.strptime("26/04/26 11:00:00", "%d/%m/%y %H:%M:%S"))

    def test_filter_value_bool_ok(self):
        filter_value = self.controller.process_filter_value("name", filter_value="true")
        self.assertTrue(filter_value)
