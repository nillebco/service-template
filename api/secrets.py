import os

import yaml

from .logger import logger

PWD = os.path.dirname(os.path.abspath(__file__))
path = f"{PWD}/../secrets/secrets.yaml"

if not os.path.exists(path):
    _raw_configuration = {}
else:
    with open(path, "r") as stream:
        _raw_configuration = yaml.safe_load(stream)


def get_secret(lowercase_secret_name: str, default=None):
    if not default:
        default = ""

    uppercase = lowercase_secret_name.upper()
    secret = _raw_configuration.get(
        lowercase_secret_name, os.environ.get(uppercase, default)
    )

    return secret


OPENAI_KEY = get_secret("openai_key")
GOOGLE_API_KEY = get_secret("google_api_key")
MISTRAL_API_KEY = get_secret("mistralai_key")
ANTHROPIC_KEY = get_secret("anthropic_key")
SIGNAL_SERVICE_URL = get_secret("signal_service_url")
WHATSAPP_SERVICE_URL = get_secret("whatsapp_service_url")
WHATSAPP_SERVICE_SECRET = get_secret("whatsapp_service_secret")
PHONE_NUMBER = get_secret("phone_number")
WEBHOOK_VERIFY_TOKEN = get_secret("webhook_verify_token")
GRAPH_API_TOKEN = get_secret("facebook_graph_api_token")
DATABASE_URL = get_secret("postgres_connection")
OWNER_NUMBER = get_secret("owner_number")

checks = {
    "OPENAI_KEY": OPENAI_KEY,
    "MISTRAL_API_KEY": MISTRAL_API_KEY,
    "PHONE_NUMBER": PHONE_NUMBER,
    "SIGNAL_SERVICE_URL": SIGNAL_SERVICE_URL,
}

for var_name, var_value in checks.items():
    if not var_value:
        logger.warning(
            "Unexpected: the variable {var_name} has the value '{var_value}'".format(
                var_name=var_name, var_value=var_value
            )
        )
