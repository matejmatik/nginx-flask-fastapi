from datetime import datetime  # noqa
from logging import getLogger  # noqa
from os import getcwd as os_getcwd, path as os_path  # noqa

from dash import Output, Input  # noqa

from ...connections import kk_client, hedge_client  # noqa
from ...core import FlaskConfiguration
from ...utils import CustomDash, format_dash_id  # noqa


# -----------------------------------------------------------------------------
# Init dash app
# -----------------------------------------------------------------------------

logger = getLogger("app." + __name__)


def initialize_dash_app(
    server: object,
    path: str,
    title: str,
    use_subpath: bool = False,
) -> CustomDash:
    app_id: str = format_dash_id(path)

    dash_app: CustomDash = CustomDash(
        title=f"{FlaskConfiguration.APP_NAME} - {title}",
        server=server,
        background_callback_manager=None,  # Default background_callback_manager, currently not used
        update_title="Stran se nalaga ...",
        routes_pathname_prefix=path,
        requests_pathname_prefix=path if use_subpath else None,
        assets_folder=os_path.join(os_getcwd(), "static") if use_subpath else "assets",
    )

    # Create the dash app layout
    dash_app.layout = create_dashboard_layout(app_id)

    # Configure the dash app event handlers
    configure_dash_event_handlers(dash_app, app_id)

    return dash_app.server


# -----------------------------------------------------------------------------
# Layout
# -----------------------------------------------------------------------------


def create_dashboard_layout(app_id: str) -> object:
    from dash.dcc import Interval, Store
    from dash.html import P
    from .elements import BeLoading, BeContainer, BeRow, BeCol

    INTERVAL_LONG = 60 * 10 * 1000  # Every 10 minutes

    return BeContainer(
        children=[
            Interval(id=f"{app_id}-interval", interval=INTERVAL_LONG, n_intervals=0),
            BeLoading(
                children=[
                    Store(
                        id=f"{app_id}-ag-grid-store",
                        storage_type="session",
                    ),
                ],
                fullscreen=True,
            ),
            # Main title
            BeRow(
                [
                    BeCol(
                        children=[
                            P(
                                "Template Dash App",
                                className="h3 p3",
                            ),
                            P(
                                "To je osnovna Dash aplikacija.",
                                className="h6 p3",
                            ),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
        shadow=False,
        className="p-3 h-100",
    )


# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


def configure_dash_event_handlers(dash_app: object, app_id: str) -> None:
    dash_app.callback(
        Output(f"{app_id}-ag-grid-store", "data"),
        Input(f"{app_id}-interval", "n_intervals"),
    )(callback_init_data)


# -----------------------------------------------------------------------------
# Callbacks functions
# -----------------------------------------------------------------------------

"""
# How to use client

from application.connections.clients import kk_client, hedge_client

kk_client.get("/info/ping")
hedge_client.get("/info/ping")

# And parse the response
"""


def callback_init_data(n_intervals: int) -> dict:
    if n_intervals > 0:
        return {}

    return {}
