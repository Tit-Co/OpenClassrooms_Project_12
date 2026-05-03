import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import patch, Mock

from click.testing import CliRunner
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cli.client_cli import client
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Commercial, Manager


class TestClientCLI(unittest.TestCase):
    main_controller = MainController()

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

    def test_create_client_ok(self):
        user = self.data.get("managers")[0]

        permissions = ["display:manager", "display:commercial", "display:technician",
                           "display:contract", "display:client", "display:event",
                           "create:client", "update:client", "delete:client", "update:contract",
                           "filter:contract", "create:event", "filter:client",
                           "filter:manager", "filter:commercial", "filter:technician"]

        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.user_controller.get_permissions = Mock(return_value=permissions)
        test_controller.view.client_view.prompt_for_client = Mock(return_value=(
            self.data["commercials"][0].id,
            "Client Test New",
            "client.test@test.com",
            "5554895623",
            "Company Test New"))

        runner.invoke(client, ["create-client"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()

        self.assertIn("✅ The client has been successfully created.", output)

    def test_create_client_returns_already_exists(self):
        user = self.data.get("managers")[0]

        permissions = ["display:manager", "display:commercial", "display:technician",
                       "display:contract", "display:client", "display:event",
                       "create:client", "update:client", "delete:client", "update:contract",
                       "filter:contract", "create:event", "filter:client",
                       "filter:manager", "filter:commercial", "filter:technician"]

        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.user_controller.get_permissions = Mock(return_value=permissions)
        test_controller.view.client_view.prompt_for_client = Mock(return_value=(
            self.data["commercials"][0].id,
            self.data["clients"][0].name,
            self.data["clients"][0].email,
            self.data["clients"][0].phone,
            self.data["clients"][0].company))

        runner.invoke(client, ["create-client"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()

        self.assertIn("❌ This client already exists.", output)
