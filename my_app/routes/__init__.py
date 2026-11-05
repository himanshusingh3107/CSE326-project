from my_app.routes.fitness_routes import fitness_api_bp
from my_app.routes.health_routes import health_bp
from my_app.routes.member_routes import member_api_bp
from my_app.routes.stats_routes import stats_api_bp
from my_app.routes.web_routes import web_bp

__all__ = [
    "web_bp",
    "member_api_bp",
    "fitness_api_bp",
    "stats_api_bp",
    "health_bp",
]
