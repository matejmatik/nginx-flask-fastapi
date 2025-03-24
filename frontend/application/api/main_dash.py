from .dash_apps import default_dash_app
from ..utils import format_dash_endpoint


def register_dash_blueprints(app):
    registered_dash_apps: list = [
        (default_dash_app, "/default-dash-app/", "Default Dash App"),
    ]

    for dash_app_setup, dash_app_url, dash_app_title in registered_dash_apps:
        # Initialize the Dash app
        app = dash_app_setup.initialize_dash_app(
            server=app,
            path=dash_app_url,
            title=dash_app_title,
        )

        # Register the Dash app as a Flask route
        app.add_url_rule(
            dash_app_url,
            endpoint=format_dash_endpoint(dash_app_url),
            view_func=lambda: app.index(),
        )
