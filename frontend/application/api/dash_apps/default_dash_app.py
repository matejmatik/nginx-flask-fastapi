from datetime import datetime  # noqa
from logging import getLogger  # noqa
from os import getcwd as os_getcwd, path as os_path  # noqa

from dash import Output, Input, Patch, State
from flask import current_app
from dash.html import P
from plotly.io import templates as plotly_templates  # noqa

from .be_dash_components import BeHiddenDashThemeSwitch, BeGraph, BeStore, BeInterval
from ...core import FlaskConfiguration
from .elements import BeLoading, BeContainer, BeRow, BeCol
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


def create_dashboard_layout(app_id: str) -> BeContainer:
    """
    create_dashboard_layout Creates the layout for the dashboard.

    """
    
    return BeContainer(
        children=[
            BeInterval(_id=f"{app_id}-app-refresh", interval_in_seconds=600),
            BeHiddenDashThemeSwitch(_id=f"{app_id}-color-mode-switch"),
            BeStore(_id=f"{app_id}-data", data={}),
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
                            BeGraph(
                                _id=f"{app_id}-graph",
                                with_loading=True,
                                loading_in_fullscreen=False,
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
    """
    Configure the dash app event handlers.
    """
    
    
    dash_app.clientside_callback(
        """
        function() {
            const storedTheme = localStorage.getItem('theme');
            if (storedTheme === 'dark') {
                return true;
            }
            else if (storedTheme === 'auto') {
                return window.matchMedia('(prefers-color-scheme: dark)').matches;
            } else {
                return false;
            }
        }
        """,
        Output(f"{app_id}-color-mode-switch", 'value'),
        Input(f"{app_id}-app-refresh", 'n_intervals'),
    )
    
    dash_app.callback(
        Output(f"{app_id}-data", "data"),
        Input(f"{app_id}-app-refresh", "n_intervals"),
    )(callback_init_data)
        
            
    
    dash_app.callback(
        Output(f"{app_id}-graph", "figure"),
        Input(f"{app_id}-color-mode-switch", "value"),
        prevent_initial_call=True,
    )(callback_update_figure_template)


# -----------------------------------------------------------------------------
# Callbacks functions
# -----------------------------------------------------------------------------



def callback_update_figure_template(switch_on: bool) -> BeGraph:

    template = plotly_templates["plotly_dark"] if switch_on else plotly_templates["plotly"]

    patched_figure = Patch()
    patched_figure["layout"]["template"] = template
    return patched_figure


def callback_init_data(n_intervals: int) -> dict:

    if n_intervals > 0:
        return {}
    return {}

