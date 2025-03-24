from flask import Blueprint

from .routes import home_blueprints

# Create the API blueprint
api_bp = Blueprint("api", __name__)

# Register individual blueprints
api_bp.register_blueprint(home_blueprints, url_prefix="/")
...
