import sys
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO

from src.controllers.collaborator_controller import CollaboratorController
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.client import Client
from src.models.contract import Contract
from src.models.event import Event
from src.models.user import Commercial, Technician


class TestCollaboratorController(unittest.TestCase):
    main_controller = MainController()
    controller = CollaboratorController(main_controller)

    credentials = {
        'email': 'admin@epicevents.url',
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

    def test_get_models(self):
        models = self.controller.get_models(self.session, "contract")

        self.assertEqual(len(models),1)
        self.assertEqual(models[0].id, self.data["contract"].id)
        self.assertEqual(models[0].client_id, self.data["client"].id)
        self.assertEqual(models[0].commercial_id, self.data["commercial"].id)
        self.assertEqual(models[0].total_amount, 100)
        self.assertEqual(models[0].bill_to_pay, 50)
        self.assertEqual(models[0].status, True)

    def test_get_model(self):
        model = self.controller.get_model(self.session, "contract", self.data["contract"].id)

        self.assertEqual(model.id, self.data["contract"].id)
        self.assertEqual(model.client_id, self.data["client"].id)
        self.assertEqual(model.commercial_id, self.data["commercial"].id)
        self.assertEqual(model.total_amount, 100)
        self.assertEqual(model.bill_to_pay, 50)
        self.assertEqual(model.status, True)

    def test_get_contract(self):
        model = self.controller.get_contract(self.session, self.data["contract"].id)

        self.assertEqual(model.id, self.data["contract"].id)
        self.assertEqual(model.client_id, self.data["client"].id)
        self.assertEqual(model.commercial_id, self.data["commercial"].id)
        self.assertEqual(model.total_amount, 100)
        self.assertEqual(model.bill_to_pay, 50)
        self.assertEqual(model.status, True)

    def test_get_client(self):
        model = self.controller.get_client(self.session, self.data["client"].id)

        self.assertEqual(model.id, self.data["client"].id)
        self.assertEqual(model.name, "Client Test")
        self.assertEqual(model.email, "client@clienttest.com")
        self.assertEqual(model.phone, 555123456)
        self.assertEqual(model.company, "Company Test")
        self.assertEqual(model.commercial_id, 1)

    def test_get_event(self):
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

        model = self.controller.get_event(self.session, event.id)

        self.assertEqual(model.id, event.id)
        self.assertEqual(model.name, "Event Test")
        self.assertEqual(model.location, "Location Test")
        self.assertEqual(model.attendees, 100)
        self.assertEqual(model.contract_id, self.data["contract"].id)
        self.assertEqual(model.technician_id, technician.id)

    def test_logout(self):
        captured_output = StringIO()
        sys.stdout = captured_output


        self.controller.logout(self.session)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You are successfully logged out.", output)
