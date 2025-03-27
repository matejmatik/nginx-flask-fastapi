from flask import Blueprint, render_template

bp = Blueprint("home_views", __name__)



@bp.route("/", methods=["GET"])
def index():
    return render_template("/home/index.jinja2")
