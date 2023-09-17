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
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("SECRET_KEY")
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"

    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'database.sqlite3'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MQTT
    MQTT_BROKER_URL = environ.get("MQTT_BROKER_URL")
    MQTT_BROKER_PORT = int(environ.get("MQTT_BROKER_PORT"))
    MQTT_KEEPALIVE = int(environ.get("MQTT_KEEPALIVE"))
