from logging import getLogger

from .sync_api_client import ApiClientDependency, SyncAPIClient


logger = getLogger(__name__)


# Currently, the API clients are initialized in here.
# This is done to avoid circular imports.
# Later on will be used as dependcy injection, which will be implemented in the future.


def initialize_api_clients() -> None:
    """
    initialize_api_clients function initializes the API clients.

    _extended_summary_

    Raises:
        e: kk_client and hedge_client initialization failed

    Returns:
        _type_: tuple(kk_client, hedge_client)
    """

    # KK API client
    kk_dependency: ApiClientDependency = ApiClientDependency(
        hostname="http://10.114.0.4:8702",
    )
    kk_client: SyncAPIClient = kk_dependency()

    try:
        logger.info(kk_client.get("/info/ping"))
    except Exception as e:
        raise e

    # Hedge API client
    hedge_dependency: ApiClientDependency = ApiClientDependency(
        hostname="http://10.114.0.3/hedg_pos_fix_prices_api/v1/",
    )
    hedge_client: SyncAPIClient = hedge_dependency()

    try:
        logger.info(hedge_client.get("/info/ping"))
    except Exception as e:
        raise e

    return kk_client, hedge_client


# kk_client, hedge_client = initialize_api_clients()
kk_client, hedge_client = None, None
