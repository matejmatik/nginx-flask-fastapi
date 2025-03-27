from os import getenv
from secrets import token_urlsafe


class FlaskConfiguration:
    # General Config
    APP_NAME = getenv("PROJECT_NAME", "Flask API")
    VERSION = getenv("PROJECT_VERSION", "0.0.0")
    DEBUG = True

    STATIC_FOLDER = getenv("STATIC_FOLDER", "static")
    TEMPLATE_FOLDER = getenv("TEMPLATE_FOLDER", "templates")

    SECRET_KEY = token_urlsafe(32)
    WTF_CSRF_ENABLED = getenv("WTF_CSRF_ENABLED", True)
    WTF_CSRF_SECRET_KEY = token_urlsafe(32)

    RECAPTCHA_PUBLIC_KEY = getenv("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = getenv("RECAPTCHA_PRIVATE_KEY")

    MYSELF_API_ENDPOINT = "http://10.114.0.4:8702"
    HEDGE_POS_API_ENDPOINT = "http://10.114.0.3/hedg_pos_fix_prices_api/v1"
