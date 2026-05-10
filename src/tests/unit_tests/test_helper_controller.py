import unittest

from src.controllers.helper_controller import is_bool, is_date, is_float


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
