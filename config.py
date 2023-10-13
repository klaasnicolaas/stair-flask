"""Flask App configuration."""
from os import environ
from pathlib import Path

from dotenv import load_dotenv

# Specificy a `.env` file containing key/value config values
basedir = Path(__file__).resolve().parent
load_dotenv(basedir / ".env")


class Config:
    """Set Flask config variables."""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # MQTT
    MQTT_BROKER_PORT = int(environ.get("MQTT_BROKER_PORT"))
    MQTT_KEEPALIVE = int(environ.get("MQTT_KEEPALIVE"))


class DevelopmentConfig(Config):
    """Set Flask config variables for development."""
    
    SOCKETIO_ASYNC_MODE = "threading"

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'database.sqlite3'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MQTT
    MQTT_BROKER_URL = environ.get("MQTT_BROKER_URL")


class TestingConfig(Config):
    """Set Flask config variables for testing."""

    TESTING = True
    MQTT_BROKER_URL = environ.get("MQTT_BROKER_URL")

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'tests' / 'test_database.sqlite3'}"


class ProductionConfig(Config):
    """Set Flask config variables for production."""

    DEBUG = False
    TESTING = False
    SOCKETIO_ASYNC_MODE = "eventlet"

    # MQTT
    MQTT_BROKER_URL = "emqx"

    # Database
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{environ.get('DB_USER')}:{environ.get('DB_PASSWORD')}@mysql:{environ.get('DB_PORT')}/{environ.get('DB_NAME')}"
