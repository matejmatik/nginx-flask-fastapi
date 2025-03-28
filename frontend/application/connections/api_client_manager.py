from json import load
from logging import getLogger
from os import getcwd, path as os_path, getenv

from flask import Flask, current_app

from .sync_api_client import SyncAPIClient
from ..core import FlaskConfiguration


logger = getLogger(__name__)


def _external_api_clients() -> list:
    """
    _external_api_clients function returns the list of external API clients.

    Returns:
        list: returns the list of external API clients
    """

    return [
        "CEEPS_API",
    ]


def __path_to_api_clients_endpoint() -> str:
    """
    __path_to_api_clients_endpoint function returns the path to the API clients configuration.

    Returns:
        str: Path to the API clients configuration
    """

    return os_path.join(
        getcwd(),
        "application",
        "config",
        FlaskConfiguration.API_CLIENTS_CONFIG_FILE,
    )


def initialize_client_connections(app: Flask) -> None:
    """
    initialize_client_connections function initializes the API clients.

    Args:
        app (Flask): Flask application
    """

    logger.info("Initializing API clients")

    # Read the API clients configuration
    try:
        with open(__path_to_api_clients_endpoint()) as f:
            api_clients = load(f)
    except FileNotFoundError as e:
        logger.error(f"API clients configuration file not found: {e}")
        raise e

    # Initialize internal API clients
    for client in api_clients:
        logger.info(f"--- Initializing {client.get('name')}")
        try:
            app.config[client.get("name")] = SyncAPIClient(
                hostname=client.get("hostname")
            )
        except Exception as e:
            logger.error(f"Failed to initialize {client.get('name')}: {e}")
            app.config[client.get("name")] = None

    # Initialize external API clients
    try:
        app.config["CEEPS_API"] = SyncAPIClient(
            hostname=getenv("SODO_SWAGGER_API_TEST_HOST"),
            username=getenv("SODO_SWAGGER_API_USER"),
            password=getenv("SODO_SWAGGER_API_PASSWORD"),
            timeout=10,
        )
    except Exception as e:
        logger.error(f"Failed to initialize CEEPS_API: {e}")

    # Check if all External API clients are initialized
    for client in _external_api_clients():
        if not app.config.get(client):
            logger.error(f"External API client {client} is not initialized")
            raise ValueError(f"External API client {client} is not initialized")

    logger.info("API clients initialized")


def disconnect_api_clients(exception: Exception) -> None:
    """
    close_api_clients function closes the API clients.
    Raises:
        e: kk_client and hedge_client closing failed

    Args:
        exception (Exception): Exception

    Returns:
        None
    """

    logger.info("Closing API clients")

    logger.error(f"Exception: {exception}")

    # Read the API clients configuration
    with open(__path_to_api_clients_endpoint()) as f:
        api_clients = load(f)

    # Close the API clients
    for client in api_clients:
        to_close_api_client = current_app.config.get(client.get("name"))
        if to_close_api_client:
            logger.info(f"--- Closing {client.get('name')}")
            to_close_api_client.close()

    for client in _external_api_clients():
        to_close_api_client = current_app.config.get(client)
        if to_close_api_client:
            logger.info(f"--- Closing {client}")
            to_close_api_client.close()

    logger.info("API clients closed")
