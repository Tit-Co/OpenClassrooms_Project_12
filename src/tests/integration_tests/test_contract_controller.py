import sys
import unittest
from datetime import datetime
from io import StringIO
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.contract_controller import ContractController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.role import Role
from src.models.user import Commercial, Technician


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)
    contract_controller = ContractController(main_controller)


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
            "commercials": [commercial, commercial_2],
            "technicians": [technician],
            "clients": [client],
            "contracts": [contract, contract_2],
            "events": [event]
        }

    def test_create_contract_with_view_ok(self) -> None:
        """
        Test for checking the method that creates contract with view in success case
        Returns:

        """
        def mock_get_models(session, model_type):
            if model_type == "client":
                return self.data["clients"]
            elif model_type == "commercial":
                return self.data["commercials"]
            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.contract_view.prompt_for_contract = Mock(return_value=[
            1, # client_id
            1, # commercial_id
            1200, # total_amount
            500, # bill to pay
            True # contract signed
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.contract_controller.create_contract_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("The contract has been successfully created.", output)

    def test_create_contract_ok(self) -> None:
        """
        Test for checking the method that creates contract with view in success case
        """
        data = {
            "client_id": 1,
            "commercial_id": 1,
            "total_amount": 10000,
            "bill_to_pay": 5000,
            "creation_date": datetime.now(),
            "status": True
        }

        self.contract_controller.create_contract(self.session, data)
        contract = self.session.query(Contract).filter_by(is_active=True,
                                                          client_id=1,
                                                          commercial_id=1,
                                                          total_amount=10000,
                                                          bill_to_pay=5000).first()

        self.assertEqual(contract.id, 3)

    def test_update_contract_with_view_ok(self) -> None:
        """
        Test for checking the method that updates contract with view in success case
        """
        def mock_get_models(session, model_type):
            if model_type == "client":
                return self.data["clients"]

            elif model_type == "commercial":
                return self.data["commercials"]

            return []

        self.controller.get_models = Mock(side_effect=mock_get_models)

        self.main_controller.view.prompt_for_model_id = Mock(return_value=1)

        self.main_controller.view.contract_view.prompt_for_contract = Mock(return_value=[
            1, # client_id
            2, # commercial_id
            15000, # total_amount
            5000, # bill to pay
            True # contract signed
        ])

        captured_output = StringIO()
        sys.stdout = captured_output

        self.contract_controller.update_contract_with_view(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        contract = self.session.query(Contract).filter_by(is_active=True, id=1).first()

        self.assertIn("The contract has been successfully updated.", output)
        self.assertEqual(contract.commercial_id, 2)
        self.assertEqual(contract.total_amount, 15000)
        self.assertEqual(contract.bill_to_pay, 5000)

    def test_update_contract_ok(self) -> None:
        """
        Test for checking the method that updates contract in success case
        """
        new_data = {
            "client_id": 1,
            "commercial_id": 1,
            "total_amount": 10000,
            "bill_to_pay": 5000,
            "status": True
        }

        self.contract_controller.update_contract(session=self.session, contract_id=1, data=new_data)
        contract = self.session.query(Contract).filter_by(is_active=True, id=1).first()

        self.assertEqual(contract.total_amount, 10000)

    def test_delete_contract_ok(self) -> None:
        """
        Test for checking the method that deletes contract in success case
        """
        self.contract_controller.delete_contract(session=self.session, contract_id=2)

        contract = self.session.query(Contract).filter_by(is_active=True, id=2).first()

        self.assertIsNone(contract)

    def test_delete_contract_impossible_ok(self) -> None:
        """
        Test for checking the method that deletes contract in failure case
        """
        self.contract_controller.delete_contract(session=self.session, contract_id=1)

        contract = self.session.query(Contract).filter_by(is_active=True, id=1).first()

        self.assertIsNotNone(contract)
