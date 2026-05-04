import unittest
from io import StringIO

from click.testing import CliRunner
from rich.console import Console
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.cli.main import cli
from src.controllers.main_controller import MainController
from src.models.base import Base
from src.models.role import Role
from src.models.user import Manager


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

        self.main_controller.init_db(self.db_engine, self.session)

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

        hashed = self.main_controller.hash_password(password=admin_credentials["password"])

        admin = Manager(name=admin_credentials["name"],
                        email=admin_credentials["email"],
                        password=hashed,
                        role_id=1
                        )
        self.session.add(admin)
        self.session.commit()

        return {
            "managers": [admin]
        }

    def test_login_ok(self):
        runner = CliRunner()

        manager = self.data["managers"][0]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.console = test_console
        self.main_controller.view.console = test_console

        password = "admin_pwd"

        runner.invoke(cli,
                      ["login", "--email", manager.email, "--password", password],
                      obj={"session": self.session,
                           "db_engine": self.db_engine,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("✅ Admin, you are successfully logged in.", output)

    def test_login_fails_with_wrong_password(self):
        runner = CliRunner()

        manager = self.data["managers"][0]

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.console = test_console
        self.main_controller.view.console = test_console

        runner.invoke(cli,
                      ["login", "--email", manager.email, "--password", "another_password"],
                      obj={"session": self.session,
                           "db_engine": self.db_engine,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("❗ Invalid password.", output)

    def test_login_fails_with_unknown_email(self):
        runner = CliRunner()

        buffer = StringIO()
        test_console = Console(file=buffer, force_terminal=False)
        self.main_controller.console = test_console
        self.main_controller.view.console = test_console

        runner.invoke(cli,
                      ["login", "--email", "another.email@another.com", "--password", "another_password"],
                      obj={"session": self.session,
                           "db_engine": self.db_engine,
                           "main_controller": self.main_controller})

        output = buffer.getvalue()

        self.assertIn("❗ This collaborator does not exist.", output)
