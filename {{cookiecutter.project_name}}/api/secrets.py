import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import logger


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Pydantic Settings automatically reads from environment variables.
    It also supports .env files natively.

    Note: Pydantic does not have native YAML support. For YAML configuration,
    you would need a third-party package like pydantic-settings-yaml.
    Environment variables are the recommended approach for secrets.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    jwt_signing_key: str = Field(default="", validation_alias="JWT_SIGNING_KEY")
    precious: str = Field(default="", validation_alias="PRECIOUS")


settings = Settings()


def get_secret(secret_name: str, default: str = "") -> str:
    """Get a secret value from environment variables.

    This function provides backward compatibility and dynamic secret access.
    For known secrets, prefer accessing them directly via the `settings` object.

    Args:
        secret_name: The name of the secret (case-insensitive).
        default: Default value if the secret is not found.

    Returns:
        The secret value from environment variables or the default.
    """
    # First try to get from settings if it's a known attribute
    attr_name = secret_name.lower()
    if hasattr(settings, attr_name):
        value = getattr(settings, attr_name)
        if value:
            return value

    # Fall back to environment variable lookup for dynamic secrets
    uppercase = secret_name.upper()
    return os.environ.get(uppercase, default)


# Export commonly used secrets for convenience
DATABASE_URL = settings.database_url

# Validation warnings
checks = {
    "DATABASE_URL": DATABASE_URL,
}

for var_name, var_value in checks.items():
    if not var_value:
        logger.warning(
            f"Unexpected: the variable {var_name} has the value '{var_value}'"
        )
