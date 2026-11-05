import sqlite3
from typing import Tuple
from flask import Blueprint, Response, current_app, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
@health_bp.route("/api/v1/health", methods=["GET"])
def health_check() -> Tuple[Response, int]:
    config = current_app.config
    database_path = config.get("DATABASE_PATH")

    database_accessible = False
    try:
        connection = sqlite3.connect(database_path, timeout=3.0)
        connection.execute("SELECT 1;")
        connection.close()
        database_accessible = True
    except Exception:
        database_accessible = False

    status_code = 200 if database_accessible else 503
    return (
        jsonify({
            "status": "UP" if database_accessible else "DEGRADED",
            "environment": config.get("ENV", "production"),
            "database_connected": database_accessible,
            "project": config.get("PROJECT_NAME"),
        }),
        status_code,
    )
