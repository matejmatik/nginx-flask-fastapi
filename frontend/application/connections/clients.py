from logging import getLogger

from flask import Flask, current_app

from ..core import FlaskConfiguration
from .sync_api_client import SyncAPIClient


logger = getLogger(__name__)


# Currently, the API clients are initialized in here.
# This is done to avoid circular imports.
# Later on will be used as dependcy injection, which will be implemented in the future.


def initialize_client_connections(app: Flask) -> None:
    """
    initialize_api_clients function initializes the API clients.

    _extended_summary_

    Raises:
        e: kk_client and hedge_client initialization failed

    Returns:
        _type_: tuple(kk_client, hedge_client)
    """

    logger.info("Initializing API clients")

    app.config["KK_API_CLIENT"] = SyncAPIClient(
        hostname=FlaskConfiguration.MYSELF_API_ENDPOINT,
    )
    app.config["HEDGE_API_CLIENT"] = SyncAPIClient(
        hostname=FlaskConfiguration.HEDGE_POS_API_ENDPOINT
    )

    logger.info("API clients initialized")


def disconnect_api_clients(exception: Exception) -> None:
    """
    close_api_clients function closes the API clients.

    _extended_summary_

    Raises:
        e: kk_client and hedge_client closing failed

    Returns:
        None
    """

    logger.info("Closing API clients")

    kk_client = current_app.config.get("KK_API_CLIENT")
    hedge_client = current_app.config.get("HEDGE_API_CLIENT")

    if kk_client:
        kk_client.close()
    if hedge_client:
        hedge_client.close()

    logger.info("API clients closed")
