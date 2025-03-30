from flask import Blueprint

from .routes import home_blueprints
from .routes import prilogaa_blueprints
from .routes import test_blueprints

# Create the API blueprint
api_bp = Blueprint("api", __name__)

# Register individual blueprints
api_bp.register_blueprint(home_blueprints, url_prefix="/")
api_bp.register_blueprint(test_blueprints, url_prefix="/test")
api_bp.register_blueprint(prilogaa_blueprints, url_prefix="/prilogaa")
