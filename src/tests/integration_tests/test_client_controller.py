import sys
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.client_controller import ClientController
from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Commercial, Manager


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)
    client_controller = ClientController(main_controller)


    @classmethod
    def setUpClass(cls) -> None:
        """
        Class method called once before test cases.
        """
        cls.db_engine = create_engine("sqlite:///:memory:")
        cls.session_test = sessionmaker(bind=cls.db_engine)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Method called after every test case.
        """
        cls.db_engine.dispose()

    def setUp(self) -> None:
        """
        Method called before every test case.
        """
        Base.metadata.drop_all(bind=self.db_engine)
        Base.metadata.create_all(bind=self.db_engine)
        self.session = self.session_test()
        self.data = self.seed_data()

    def tearDown(self) -> None:
        """
        Method called once after all test cases.
        """
        self.session.close()

    def seed_data(self) -> dict:
        """
        Method to seed data for testing.
        Returns:
        A dictionary with seed data.
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

        client_2 = Client(name="Another Client Test",
                        email="client2@clienttest.com",
                        phone="5551248966",
                        company="Company Test 2",
                        creation_date=datetime.now(),
                        last_update=datetime.now(),
                        commercial_id=commercial.id)

        self.session.add(client)
        self.session.add(client_2)
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
            "managers": [manager],
            "commercials": [commercial],
            "clients": [client, client_2],
            "contracts": [contract]
        }

    def test_create_client_with_view_ok(self) -> None:
        """
        Test for checking the method that creates a new client with view.
        """
        def mock_get_models(session):
            return self.data["commercials"]

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.client_view.prompt_for_client = Mock(return_value=[
            "Client_test",
            "client@client.com",
            "3355659845",
            "Company test",
            1
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.client_controller.create_client_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("The client has been successfully created.", output)

    def test_create_client_ok(self) -> None:
        """
        Method to check the method that creates a new client.
        """
        data = {
            "name": "Client Test",
            "email": "client@client.com",
            "phone": "3355659845",
            "company": "Company test",
            "creation_date": datetime.now(),
            "last_update": datetime.now(),
            "commercial_id": 1
        }

        self.client_controller.create_client(self.session, data)
        client = self.session.query(Client).filter_by(is_active=True, email="client@client.com").first()

        self.assertEqual(client.id, 3)

    def test_update_client_with_view_ok(self) -> None:
        """
        Test for checking the method that updates a client with view.
        """
        def mock_get_models(session, model_type):
            if model_type == "commercial":
                return self.data["commercials"]
            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)

        self.main_controller.view.client_view.prompt_for_client = Mock(return_value=[
            1,
            "Client Updated",
            "new.client@client.com",
            "3355679845",
            "Company test update",
            ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.client_controller.update_client_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        client = self.session.query(Client).filter_by(is_active=True, id=1).first()

        self.assertIn("The client has been successfully updated.", output)
        self.assertEqual(client.name, "Client Updated")
        self.assertEqual(client.email, "new.client@client.com")
        self.assertEqual(client.phone, "3355679845")
        self.assertEqual(client.company, "Company test update")

    def test_update_client_ok(self) -> None:
        """
        Test for checking the method that updates a client.
        """
        new_data = {
            "name": "Client Test",
            "email": "client@client.com",
            "phone": "3355659845",
            "company": "Company test",
            "creation_date": datetime.now(),
            "last_update": datetime.now(),
            "commercial_id": 1
        }

        self.client_controller.update_client(session=self.session, client_id=1, data=new_data)
        client = self.session.query(Client).filter_by(is_active=True, id=1).first()

        self.assertEqual(client.email, "client@client.com")

    def test_delete_client_ok(self) -> None:
        """
        Test for checking the method that deletes a client.
        """
        self.client_controller.delete_client(session=self.session, client_id=2)

        client = self.session.query(Client).filter_by(is_active=True, id=2).first()

        self.assertIsNone(client)

    def test_delete_client_impossible_ok(self) -> None:
        """
        Test for checking the method that deletes a client when it's not possible.
        """
        self.client_controller.delete_client(session=self.session, client_id=1)

        client = self.session.query(Client).filter_by(is_active=True, id=1).first()

        self.assertIsNotNone(client)

    def test_filter_client_ok(self) -> None:
        """
        Test for checking the method that creates collaborator with view
        """
        clients = self.client_controller.filter_client(session=self.session,
                                                        my_filter="name",
                                                        filter_value="Client Test",
                                                        class_name=Client)

        self.assertEqual(clients, self.data["clients"])

    def test_filter_client_returns_empty_list(self) -> None:
        """
        Test for checking the method that creates collaborator with view
        """
        clients = self.client_controller.filter_client(session=self.session,
                                                        my_filter="name",
                                                        filter_value="machin",
                                                        class_name=Client)

        self.assertEqual(clients, [])
