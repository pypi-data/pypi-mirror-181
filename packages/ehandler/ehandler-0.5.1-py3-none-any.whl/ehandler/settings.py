# Built-In
from typing import Any

# Third-Party
from pydantic import BaseSettings, validator

# Internal
from ehandler.utils import fetch, fetch_metadata


class Settings(BaseSettings):
    """
    Base settings

    :param service: Cloud Run service name, get from metadata env variables server
    :param revision: Cloud Run revision name, get from metadata env variables server

    See Also:
        - https://cloud.google.com/run/docs/container-contract#services-env-vars
    """

    SERVICE: str | None
    SERVER_IP: str | None
    PROJECT_ID: str | None

    TIMEOUT: float = 2  # Write in seconds read in nanoseconds

    LOG_LEVEL: str = "INFO"
    VERBOSITY: int = 4
    DEBUG: bool = False

    @validator("PROJECT_ID", always=True)
    @classmethod
    def _project_id(cls, value: str | None, values: dict[str, Any]) -> str | None:
        """
        Get project id from metadata server
        """
        if value:
            return value
        return fetch_metadata("project/project-id") or values.get("SERVICE")

    @validator("SERVER_IP", always=True)
    @classmethod
    def _server_ip(cls, value: str | None) -> str | None:
        """
        Get public IP
        """
        if value:
            return value
        url = "https://curlmyip.org/"
        return fetch(url)

    @validator("TIMEOUT")
    @classmethod
    def _timeout(cls, value: float) -> float:
        """
        Convert from seconds to nanoseconds
        """
        return value * 1e9

    class Config:
        """
        Base settings config
        """

        env_prefix = "EHANDLER_"
        env_file = ".env"
        fields = {"SERVICE": {"env": "K_SERVICE"}}


settings = Settings()  # type: ignore
