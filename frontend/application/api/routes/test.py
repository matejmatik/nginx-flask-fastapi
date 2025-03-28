from flask import Blueprint, current_app, jsonify


bp = Blueprint("test_views", __name__)


@bp.route("/kk/ping", methods=["GET"])
def kk_ping():
    kk_client = current_app.config["KK_API_CLIENT"]

    return jsonify(kk_client.get("/info/ping"))


@bp.route("/hedge/ping", methods=["GET"])
def hedge_ping():

    hedge_client = current_app.config["HEDGE_API_CLIENT"]

    return jsonify(hedge_client.get("/info/ping"))


@bp.route("/edc-lifecycle/ping", methods=["GET"])
def edc_lifecycle_ping():

    edc_lifecycle_client = current_app.config["EDC_LIFECYCLE_API"]

    return jsonify(edc_lifecycle_client.get("/info/ping"))
