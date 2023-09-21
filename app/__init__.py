"""Initialize Stair Challenge app."""
# ruff: noqa: E402, ARG001
import getpass
import json
from datetime import datetime, timedelta

from flask import Flask, redirect, request, session, url_for
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from rpi_ws281x import Color
from sqlalchemy import exc

from app.const import MQTT_STATUS_TOPIC, MQTT_TRIGGER_TOPIC
from app.led_controller import Colors, LEDController
from app.mqtt_controller import MQTTClient
from config import Config

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")

# Load config values from app/config.py
app.config.from_object(Config)

# Database configuration
db = SQLAlchemy(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "auth.login"


@app.before_request
def make_session_permanent():
    """Make the session permanent."""
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=12)


# Initialize MQTT client
mqtt = MQTTClient()
mqtt.connect()

from app.blueprints.auth.models import User
from app.blueprints.backend.models import Sensor

workout_active: bool = False

# ----------------------------------------------------------------------------#
# LED strip configuration.
# ----------------------------------------------------------------------------#
LED_COUNT = 104  # Number of LED pixels.
LED_PIN = 10  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

led_controller = LEDController(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_BRIGHTNESS,
    LED_INVERT,
    LED_CHANNEL,
)
led_controller.turn_off()

# Install the blueprints
from app.blueprints.auth import bp as auth_bp
from app.blueprints.backend import bp as backend_bp
from app.blueprints.frontend import bp as frontend_bp

app.register_blueprint(frontend_bp)
app.register_blueprint(backend_bp, url_prefix="/admin")
app.register_blueprint(auth_bp)


@app.cli.command("create_admin")
def create_admin() -> None:
    """Create a new admin user."""
    name = input("Enter name: ")
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(
            name=name,
            email=email,
            password=password,
            is_admin=True,
            created_at=datetime.now(),
        )
        db.session.add(user)
        db.session.commit()
        print(f"Admin with email {email} created successfully!")
    except Exception as e:
        print(f"Could not create admin: {e}")
        db.session.rollback()
        return 1


def on_topic_trigger(
    client: MQTTClient,
    userdata: dict,
    message: dict,
) -> None:
    """MQTT function to handle trigger messages.

    Args:
    ----
        client: The client instance for this callback.
        userdata: The private user data as set in Client() or userdata_set().
        message: An instance of MQTTMessage.
    """
    colors = Colors()
    if workout_active:
        led_controller.set_color(
            colors.get_random_unique_color(),
        )
    # TODO: Check welke workout er actief is en pas een if statement toe
    # INFO: Call daarna de functie om de LED strip aan te sturen
    print(f"Message Received from Others: {message.payload.decode()}")


def on_topic_status(
    client: MQTTClient,
    userdata: dict,
    message: dict,
) -> None:
    """MQTT Function to handle status messages.

    Args:
    ----
        client: The client instance for this callback.
        userdata: The private user data as set in Client() or userdata_set().
        message: An instance of MQTTMessage.
    """
    # TODO: Socket emit to update sensot status to specific element ID
    try:
        data = json.loads(message.payload)
        with app.app_context():
            sensor = Sensor.query.filter_by(
                client_id=f"sensor-{data['client_id']}",
            ).first()
            if sensor:
                # If the sensor already exists
                # print(f"Updating sensor: {data['client_id']}")
                sensor.ip_address = data["ip_address"]
                sensor.max_distance = data["max_distance"]
                sensor.threshold = data["threshold"]
                sensor.status = data["status"]
                sensor.last_update = datetime.now()
                db.session.commit()
            else:
                # If the sensor doesn't exist
                print(f"Adding new sensor: {data['client_id']}")
                sensor = Sensor(
                    client_id=f"sensor-{data['client_id']}",
                    ip_address=data["ip_address"],
                    max_distance=data["max_distance"],
                    threshold=data["threshold"],
                    status=data["status"],
                    last_update=datetime.now(),
                )
                db.session.add(sensor)
                db.session.commit()
    except exc.IntegrityError:
        with app.app_context():
            db.session.rollback()
        print("An error occurred during database operation.")


# Routes
@app.route("/set_color", methods=["GET"])
def set_color() -> None:
    """Set LED strip color."""
    args = request.args
    led_controller.set_color(
        Color(int(args.get("red")), int(args.get("green")), int(args.get("blue"))),
    )
    return redirect(url_for("backend.led_control"))


@app.route("/turn_off")
def turn_off() -> None:
    """Turn off LED strip."""
    led_controller.turn_off()
    return redirect(url_for("backend.led_control"))


# SocketIO events
@socketio.on("connect")
def on_connect():
    """SocketIO function to handle connect event."""
    print("Client connected")


@socketio.on("active")
def on_system_active(event):
    """Put the system in active mode or not."""
    global workout_active

    if event["data"] == "start":
        workout_active = True
        print("Starting workout")
    elif event["data"] == "stop":
        workout_active = False
        led_controller.turn_off()
        print("Stopping workout")


@socketio.on("restart_sensors")
def on_restart_sensors(event):
    """SocketIO function to handle restart_sensors event."""
    print(f"Restarting sensors - {event}")
    # TODO: Send restart signal to single sensor or all sensors


# MQTT events
mqtt.client.message_callback_add(MQTT_TRIGGER_TOPIC, on_topic_trigger)
mqtt.client.message_callback_add(MQTT_STATUS_TOPIC, on_topic_status)
