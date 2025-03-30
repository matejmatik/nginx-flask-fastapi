from flask import Blueprint, current_app, jsonify
from flask_login import login_required

from ...connections import SyncAPIClient

bp = Blueprint("test_views", __name__)


@bp.route("/kk/ping", methods=["GET"])
@login_required
def kk_ping() -> None:
    """
    kk_ping function is used to test the connection to the KK API.
    It returns a JSON response with the status of the connection.

    Returns:

    """

    kk_client: SyncAPIClient = current_app.config["KK_API_CLIENT"]

    return jsonify(kk_client.get("/info/ping"))


@bp.route("/hedge/ping", methods=["GET"])
@login_required
def hedge_ping() -> None:
    """
    hedge_ping function is used to test the connection to the Hedge API.
    It returns a JSON response with the status of the connection.

    Returns:

    """

    hedge_client: SyncAPIClient = current_app.config["HEDGE_API_CLIENT"]

    return jsonify(hedge_client.get("/info/ping"))


@bp.route("/edc-lifecycle/ping", methods=["GET"])
@login_required
def edc_lifecycle_ping() -> None:
    """
    edc_lifecycle_ping function is used to test the connection to the EDC lifecycle API.
    It returns a JSON response with the status of the connection.


    Returns:
        JSON response with the status of the connection.
    """

    edc_lifecycle_client: SyncAPIClient = current_app.config["EDC_LIFECYCLE_API"]

    return jsonify(edc_lifecycle_client.get("/info/ping"))


@bp.route("/prilogga/ping", methods=["GET"])
@login_required
def prilogga_ping() -> None:
    """
    prilogga_ping function is used to test the connection to the Prilogaa API.
    It returns a JSON response with the status of the connection.

    Returns:
        JSON response with the status of the connection.
    """

    prilogaa_client: SyncAPIClient = current_app.config["PRILOGAA_API"]

    return jsonify(prilogaa_client.get("/info/ping"))
