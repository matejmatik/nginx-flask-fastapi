from flask import Flask
from flask_login import LoginManager, current_user
from jinja_partials import register_extensions as jinja_partials_register_extensions

from .api import api_blueprints, register_api_error_handlers, register_dash_blueprints
from .auth import User
from .connections import initialize_client_connections
from .core import FlaskConfiguration, RedisCache
from .utils import CustomRequest


def _initialize_login_manager(app: Flask) -> None:
    """
    _initialize_login_manager Initializes the login manager for the Flask application.
    """

    lrm: LoginManager = LoginManager()
    lrm.login_view = "api.home_views.login"
    lrm.login_message = "Za dostop do te strani morate biti prijavljeni."
    lrm.init_app(app)  # set up login manager

    @lrm.user_loader
    def load_user(email: str) -> User:
        return User().query_users(email)

    @lrm.request_loader
    def request_loader(request: CustomRequest) -> User:
        email = request.form.get("email")
        return User().query_users(email)

    @app.context_processor
    def inject_user() -> dict:
        # Inject the current user into the Jinja templates
        return dict(user=current_user)


def initialize_flask_application() -> Flask:
    # Initialize the Flask application
    app = Flask(__name__, instance_relative_config=True)

    # Load the configuration
    with app.app_context():
        # Load the configuration from the config file
        RedisCache.init_app(app)
        app.config.from_object(FlaskConfiguration)

        # Add other configurations
        jinja_partials_register_extensions(app)
        initialize_client_connections(app)
        register_dash_blueprints(app)
        app.register_blueprint(api_blueprints, url_prefix="/")
        register_api_error_handlers(app)
        _initialize_login_manager(app)

        @app.context_processor
        def __inject_version() -> dict:
            return dict(version=FlaskConfiguration.VERSION)

    return app


app = initialize_flask_application()
app.request_class = CustomRequest

# @app.teardown_appcontext
# def __disconnect_api_clients(exception: Exception) -> None:
#     disconnect_api_clients(exception)
