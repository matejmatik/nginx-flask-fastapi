from os import getenv
from secrets import token_urlsafe


class FlaskConfiguration:
    # General Config
    APP_NAME: str = getenv("PROJECT_NAME", "Flask API")
    VERSION: str = getenv("PROJECT_VERSION", "0.0.0")
    DEBUG: bool = True

    STATIC_FOLDER: str = getenv("STATIC_FOLDER", "static")
    TEMPLATE_FOLDER: str = getenv("TEMPLATE_FOLDER", "templates")

    SECRET_KEY: str = token_urlsafe(32)
    WTF_CSRF_ENABLED: bool = getenv("WTF_CSRF_ENABLED", True)
    WTF_CSRF_SECRET_KEY: str = token_urlsafe(32)

    RECAPTCHA_PUBLIC_KEY: str = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY: str = getenv("RECAPTCHA_PRIVATE_KEY")

    API_CLIENTS_CONFIG_FILE: str = "api_clients_endpoint.json"
