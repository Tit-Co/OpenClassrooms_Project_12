import unittest

from src.controllers.helper_controller import is_bool, is_date, is_float, is_models_empty
from src.models.client import Client
from src.models.contract import Contract
from src.models.user import Commercial


class TestHelperController(unittest.TestCase):

    def test_is_float_ok(self) -> None:
        """
        Test for checking the is_float method in a True case
        """
        float = is_float(s="152.23")

        self.assertTrue(float)

    def test_is_float_return_false_with_str(self) -> None:
        """
        Test for checking the is_float method in a false case
        """
        float = is_float(s="test")

        self.assertFalse(float)

    def test_is_date_ok(self) -> None:
        """
        Test for checking the is_date method in a success case
        """
        date = is_date(s="25/04/26 11:00")

        self.assertTrue(date)

    def test_is_date_return_false_with_wrong_format(self) -> None:
        """
        Test for checking the is_date method in a failure case
        """
        date = is_date(s="25/04/26 11")

        self.assertFalse(date)

    def test_is_bool(self) -> None:
        """
        Test for checking the is_bool method in a success case
        """
        my_bool = is_bool(s="true")

        self.assertTrue(my_bool)

    def test_is_bool_fails(self) -> None:
        """
        Test for checking the is_bool method in a failure case
        """
        my_bool = is_bool(s="test")

        self.assertFalse(my_bool)

    def test_is_models_clients_empty_returns_true(self) -> None:
        """
        Test for checking the is_models_empty method in a success case
        """
        clients = []
        my_bool = is_models_empty(models=clients)

        self.assertTrue(my_bool)

    def test_is_models_clients_empty_returns_false(self) -> None:
        """
        Test for checking the is_models_empty method in a false case with clients
        """
        client = Client(name="Client Test",
                        email="client@clienttest.com",
                        phone="555123456",
                        company="Company Test",
                        commercial_id=1)
        clients = [client]
        my_bool = is_models_empty(models=clients)

        self.assertFalse(my_bool)

    def test_is_models_contracts_empty_returns_false(self) -> None:
        """
        Test for checking the is_models_empty method in a false case with contracts
        """
        commercial = Commercial(name="Commercial name",
                                email="commercial.test@epicevents.url.com",
                                password="pwd_test",
                                role_id=2)

        client = Client(name="Client Test",
                        email="client@clienttest.com",
                        phone="555123456",
                        company="Company Test",
                        commercial_id=commercial.id)

        contract = Contract(client_id=client.id,
                            commercial_id=commercial.id,
                            total_amount=100,
                            bill_to_pay=50,
                            status=True)

        contracts = {
            "contracts": [contract],
            "clients": [client],
            "commercials": [commercial]
        }

        my_bool = is_models_empty(models=contracts)

        self.assertFalse(my_bool)
