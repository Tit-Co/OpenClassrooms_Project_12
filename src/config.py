import os

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DATABASE")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

APP_ENV = os.getenv("APP_ENV", "dev")
SENTRY_KEY = os.getenv("SENTRY_KEY")
