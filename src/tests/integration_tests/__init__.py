from unittest.mock import patch


patcher = patch(
    "src.core.monitoring.sentry_sdk.init",
    return_value=None
)

patcher.start()
