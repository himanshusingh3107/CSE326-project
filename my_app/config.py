import os
from pathlib import Path
from typing import Type
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class BaseConfig:
    PROJECT_NAME: str = "Veer Batalion Gym Management System"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-veer-batalion-98234")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "5000"))
    DEBUG: bool = False
    TESTING: bool = False

    DATABASE_PATH: Path = BASE_DIR / os.getenv("DATABASE_FILE", "gym_database.sqlite")
    SEED_DATA_PATH: Path = BASE_DIR / "members_data.json"

    TEMPLATE_DIR: Path = BASE_DIR / "templates"
    STATIC_DIR: Path = BASE_DIR / "static"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    JSON_SORT_KEYS: bool = False


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"


class TestingConfig(BaseConfig):
    TESTING: bool = True
    DEBUG: bool = True
    DATABASE_PATH: Path = BASE_DIR / "test_gym_database.sqlite"


CONFIGURATION_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> Type[BaseConfig]:
    environment_name = os.getenv("FLASK_ENV", "development").lower()
    return CONFIGURATION_MAP.get(environment_name, DevelopmentConfig)
