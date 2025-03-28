from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, login_user, logout_user, current_user

from ...auth import User, validate_user_password
from ...forms import LoginForm
from ...utils import flash_form_errors

bp = Blueprint("home_views", __name__)


@bp.route("/", methods=["GET"])
@login_required
def index():
    if current_user.is_authenticated:
        return render_template("/home/index.jinja2")
    else:
        return redirect(url_for("api.home_views.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if request.method == "POST":
        if login_form.validate_on_submit():
            # Get form data
            form_data = login_form.data
            # Query user
            user: User = User().query_users(form_data.get("email"))
            # Validate user password
            if user is not None and validate_user_password(
                user=user, password=form_data.get("password")
            ):
                flash("Uspešno ste se prijavili!", category="success")
                login_user(user, remember=form_data.get("remember_me"))
                return redirect(url_for("api.home_views.index"))
            else:
                flash("Napačno uporabniško ime ali geslo!", category="danger")
        else:
            # Problem with form data
            flash_form_errors(login_form)

    return render_template("/home/login.jinja2", form=login_form)


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("api.home_views.login"))


@bp.route("/iskanje", methods=["POST"])
@login_required
def search():
    # search_string and search_category
    global_search = request.form
    search_term = global_search.get("g_search_string", "")
    search_category = global_search.get("g_search_category", "all")

    search_results = []

    return render_template(
        "shared/tables/global_search_results.jinja2",
        search_results=search_results,
    )
