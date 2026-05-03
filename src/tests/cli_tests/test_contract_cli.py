import unittest

from datetime import datetime
from io import StringIO
from unittest.mock import patch, Mock

from click.testing import CliRunner
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cli.contract_cli import contract
from src.controllers.main_controller import MainController
from src.models.client import Client
from src.models.contract import Contract
from src.models.user import Manager, Commercial
from src.models.base import Base


class TestContractCLI(unittest.TestCase):
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

        commercial_2 = Commercial(name="Commercial name 2",
                                  email="commercial2.test@epicevents.url.com",
                                  password="pw_test",
                                  role_id=2)

        self.session.add(commercial)
        self.session.add(commercial_2)
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

        return {
            "managers": [admin],
            "clients": [client],
            "commercials": [commercial, commercial_2],
            "contracts": [contract, contract_2]
        }

    def test_display_contract_ok(self):
        runner = CliRunner()

        test_session = self.session
        test_controller = self.main_controller

        user = self.data.get("managers")[0]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        test_controller.user_controller.get_current_user = Mock(return_value=user)
        test_controller.view.prompt_for_model_id_with_action = Mock(return_value=1)

        runner.invoke(contract, ["display-contract"],
                      obj={"session": test_session, "main_controller": test_controller})

        output = buffer.getvalue()
        self.assertIn("CONTRACTS TO DISPLAY", output)
        self.assertIn("Here is the contract n°1", output)
        self.assertIn("Client name : Client Test", output)
        self.assertIn("Total amount : 100.0", output)
