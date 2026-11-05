from typing import Tuple
from flask import Blueprint, Response, current_app, jsonify
from my_app.services.member_service import MemberService

stats_api_bp = Blueprint("stats_api", __name__, url_prefix="/api/v1/stats")


@stats_api_bp.route("", methods=["GET"])
def get_gym_statistics() -> Tuple[Response, int]:
    service: MemberService = current_app.extensions["member_service"]
    metrics = service.get_dashboard_metrics()

    return jsonify({"success": True, "data": metrics}), 200
