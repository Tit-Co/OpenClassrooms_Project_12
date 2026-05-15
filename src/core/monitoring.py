import logging
import sentry_sdk

from sentry_sdk.integrations.logging import LoggingIntegration

from src.config import APP_ENV, SENTRY_KEY

logger = logging.getLogger(__name__)


def init_sentry():
    logging.basicConfig(level=logging.CRITICAL)

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.INFO,
    )

    if APP_ENV != "test":
        sentry_sdk.init(
            dsn=SENTRY_KEY,
            # Add request headers and IP for users,
            # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
            send_default_pii=True,

            # Enable logs to be sent to Sentry
            enable_logs=True,

            integrations=[sentry_logging]
        )


def sentry_capture_exception(error: Exception):
    sentry_sdk.capture_exception(error)


def sentry_capture_message(s: str):
    sentry_sdk.capture_message(s)


def sentry_flush():
    sentry_sdk.flush(timeout=2)
