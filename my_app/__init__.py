import logging
from typing import Optional, Type
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from my_app.config import BaseConfig, get_config
from my_app.exceptions import AppException
from my_app.repositories.member_repository import MemberRepository
from my_app.routes import fitness_api_bp, health_bp, member_api_bp, stats_api_bp, web_bp
from my_app.services.fitness_service import FitnessService
from my_app.services.member_service import MemberService


def setup_logging(log_level: str) -> None:
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    log_format = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(level=numeric_level, format=log_format, datefmt=date_format, force=True)


def register_error_handlers(app: Flask) -> None:
    logger = logging.getLogger("my_app.error_handler")

    @app.errorhandler(AppException)
    def handle_custom_app_exception(exception: AppException):
        logger.warning(
            f"Handled application exception: {exception.error_code} - {exception.message} "
            f"[Route: {request.method} {request.path}]"
        )
        return jsonify(exception.to_dict()), exception.status_code

    @app.errorhandler(HTTPException)
    def handle_standard_http_exception(exception: HTTPException):
        if request.path.startswith("/api/"):
            return (
                jsonify({
                    "success": False,
                    "error": {
                        "code": exception.name.upper().replace(" ", "_"),
                        "message": exception.description,
                    },
                }),
                exception.code or 500,
            )
        return exception

    @app.errorhandler(Exception)
    def handle_unhandled_exception(exception: Exception):
        logger.error(
            f"Unhandled exception during {request.method} {request.path}: {str(exception)}",
            exc_info=True,
        )
        return (
            jsonify({
                "success": False,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected internal server error occurred.",
                },
            }),
            500,
        )


def create_app(config_class: Optional[Type[BaseConfig]] = None) -> Flask:
    active_config = config_class or get_config()

    setup_logging(active_config.LOG_LEVEL)
    logger = logging.getLogger("my_app.factory")

    app = Flask(
        __name__,
        template_folder=str(active_config.TEMPLATE_DIR),
        static_folder=str(active_config.STATIC_DIR),
    )
    app.config.from_object(active_config)

    CORS(app)

    member_repository = MemberRepository(
        database_path=active_config.DATABASE_PATH,
        seed_data_path=active_config.SEED_DATA_PATH,
    )
    member_service = MemberService(repository=member_repository)
    fitness_service = FitnessService()

    app.extensions["member_repository"] = member_repository
    app.extensions["member_service"] = member_service
    app.extensions["fitness_service"] = fitness_service

    app.register_blueprint(web_bp)
    app.register_blueprint(member_api_bp)
    app.register_blueprint(fitness_api_bp)
    app.register_blueprint(stats_api_bp)
    app.register_blueprint(health_bp)

    register_error_handlers(app)

    logger.info(
        f"Application initialized successfully in '{app.config.get('ENV', 'development')}' mode. "
        f"Database target: {active_config.DATABASE_PATH}"
    )

    return app
