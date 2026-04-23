import unittest

import bcrypt

from src.controllers.main_controller import MainController


class TestMainController(unittest.TestCase):
    controller = MainController()

    credentials = {
        'password': 'tgl_Prn_C1'
    }

    def test_init_super_user_ok(self) -> None:
        """
        Test for checking the initialization of the super user
        """
        super_user_dict = self.controller.init_super_user()

        self.assertIn('name', super_user_dict)
        self.assertIn('email', super_user_dict)
        self.assertIn('password', super_user_dict)
        self.assertIn('role', super_user_dict)

    def test_hash_password_ok(self) -> None:
        """
        Test for checking the method that hashes the password
        """
        password = self.credentials.get('password')

        hashed = self.controller.hash_password(password)
        checked = bcrypt.checkpw(password.encode("utf-8"), hashed)

        self.assertTrue(checked)

    def test_check_password_ok(self) -> None:
        """
        Test for checking the method that checks the password
        """
        password = self.credentials.get('password')

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        checked = self.controller.check_password(password, hashed.decode("utf-8"))

        self.assertTrue(checked)
