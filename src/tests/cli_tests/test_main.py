import unittest
from io import StringIO

from click.testing import CliRunner
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cli.main import cli
from src.controllers.main_controller import MainController
from src.models.user import Manager
from src.models.base import Base


class TestCLI(unittest.TestCase):
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

        return {
            "managers": [admin]
        }

    def test_login_ok(self):
        runner = CliRunner()

        managers = self.data.get("managers")

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        runner.invoke(cli, ["login", "--email", managers[0].email, "--password", managers[0].password],
                      obj={"session": self.session,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("Admin, you are successfully logged in", output)

    def test_login_fails_with_wrong_password(self):
        runner = CliRunner()

        managers = self.data.get("managers")

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        runner.invoke(cli, ["login", "--email", managers[0].email, "--password", "another_password"],
                      obj={"session": self.session,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("Invalid password", output)

    def test_login_fails_with_unknown_email(self):
        runner = CliRunner()

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.view.console = test_console

        runner.invoke(cli, ["login", "--email", "another.email@another.com", "--password", "another_password"],
                      obj={"session": self.session,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("This collaborator does not exist", output)
