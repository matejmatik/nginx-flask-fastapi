from logging import getLogger
from os import getenv
from secrets import token_urlsafe
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


logger = getLogger(__name__)


def parse_cors(v: Any) -> list[str] | str:
    # Parse a string of origins to a list of origins
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    PATH_TO_SQL_QUERY: str = "sql"

    ENVIRONMENT: Literal["local", "development", "production"] = getenv(
        "ENVIRONMENT", "local"
    )
    PROJECT_NAME: str
    PROJECT_VERSION: str
    DESCRIPTION: str = "Project description ..."

    @computed_field
    @property
    def DEBUG(self) -> bool:
        if self.ENVIRONMENT in ["local", "development"]:
            return True
        return False

    # --- BACKEND API ---
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"
    BACKEND_PORT: int
    BACKEND_HEALTH_CHECK_PATH: str = "/info/health-check"

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development

        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    # --- REDIS ---
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @computed_field  # type: ignore[misc]
    @property
    def REDIS_BASE(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @computed_field  # type: ignore[misc]
    @property
    def REDIS_URL(self) -> str:
        return f"{self.REDIS_BASE}/0"

    @computed_field  # type: ignore[misc]
    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"{self.REDIS_BASE}/1"

    @computed_field  # type: ignore[misc]
    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"{self.REDIS_BASE}/2"

    # --- EMAILS ---

    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.EMAILS_FROM_EMAIL)

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                logger.warning(message)
            else:
                raise ValueError(message)

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """
        _enforce_non_default_secrets is a model validator that checks if the secret keys are still the default ones.
        """

        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)

        return self


settings = Settings()  # type: ignore
