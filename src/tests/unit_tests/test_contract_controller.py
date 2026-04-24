import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.contract_controller import ContractController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.role import Role
from src.models.user import Commercial, Manager


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)
    contract_controller = ContractController(main_controller)

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

        self.session.add(contract)
        self.session.commit()


        return {
            "managers": [manager],
            "commercials": [commercial],
            "clients": [client],
            "contracts": [contract]
        }

    def test_get_contract(self) -> None:
        """
        Test for checking the method that gets a contract.
        """
        contract = self.contract_controller.get_contract(self.session, 1)

        self.assertEqual(contract.id, self.data["contracts"][0].id)
