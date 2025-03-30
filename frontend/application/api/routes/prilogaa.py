from flask import Blueprint, render_template, current_app, flash
from flask_login import login_required

from ...core import cache
from ...connections import SyncAPIClient

bp = Blueprint("prilogaa_views", __name__)


def __get_priloge_a_table_data() -> list[dict]:
    """
    __get_priloga_table_data is used to fetch the list of all priloge_a from the API.

    _extended_summary_

    Returns:
        list[dict]: _description_
    """

    prilogaa_client: SyncAPIClient = current_app.config["PRILOGAA_API"]
    try:
        priloge_a_list = prilogaa_client.get("/prilogaa/kk", params={}).get("data", [])
        if len(priloge_a_list) == 0:
            flash("Ni nobenih podatkov", "warning")
    except Exception as e:
        flash(f"Napaka pri pridobivanju podatkov: {str(e)}", "danger")
        priloge_a_list = []

    return priloge_a_list


def __get_priloga_a_details_data(priloga_a_desc_id: int) -> dict:
    """
    __get_priloga_details_data is used to fetch the details of a specific
    priloga_a_desc_id from the API. It uses the SyncAPIClient to make a GET

    Args:
        priloga_a_desc_id (int): Argument to get the details of a specific priloga_a_desc_id.

    Returns:
        dict: A dictionary containing the details of the specific priloga_a_desc_id.
    """

    prilogaa_client: SyncAPIClient = current_app.config["PRILOGAA_API"]
    try:
        prilogaa_details = prilogaa_client.get(
            f"/prilogaa/details/{priloga_a_desc_id}",
            params={"priloga_a_desc_id": priloga_a_desc_id},
        ).get("data", {})
        if not prilogaa_details:
            flash("Ni nobenih podatkov", "warning")
    except Exception as e:
        flash(f"Napaka pri pridobivanju podatkov: {str(e)}", "danger")
        prilogaa_details = {}

    return prilogaa_details


@bp.route("/", methods=["GET"])
@login_required
@cache.cached(timeout=600)
def index():
    try:
        return render_template(
            "/prilogaa/index.jinja2",
            priloge_a_list=__get_priloge_a_table_data(),
        )
    except Exception as e:
        flash(f"Napaka pri nalaganju strani: {str(e)}", "danger")
        return render_template(
            "/prilogaa/index.jinja2",
            priloge_a_list=[],
        )


@bp.route("/podrobno/<path:priloga_a_desc_id>", methods=["GET"])
@login_required
def prilogaa_read(priloga_a_desc_id: int) -> object:
    return render_template(
        "prilogaa/details_priloga_a.jinja2",
        priloga_a=__get_priloga_a_details_data(priloga_a_desc_id),
        priloga_a_desc_id=priloga_a_desc_id,
    )
