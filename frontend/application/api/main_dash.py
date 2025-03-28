from flask import redirect, url_for, request
from flask_login import current_user

from .dash_apps import default_dash_app
from ..utils import format_dash_endpoint


def register_dash_blueprints(app):
    registered_dash_apps: list = [
        (default_dash_app, "/default-dash-app/", "Default Dash App", "cat:default")
    ]

    for dash_app_setup, dash_app_url, dash_app_title, category in registered_dash_apps:
        # Initialize the Dash app
        app = dash_app_setup.initialize_dash_app(
            server=app,
            path=dash_app_url,
            title=dash_app_title,
        )

        @app.before_request
        def check_login():
            if (
                request.path.startswith(dash_app_url)
                and not current_user.is_authenticated
            ):
                return redirect(url_for("api.home_views.login"))

        # Register the Dash app as a Flask route
        app.add_url_rule(
            dash_app_url,
            endpoint=format_dash_endpoint(dash_app_url),
            view_func=lambda: app.index(),
        )
