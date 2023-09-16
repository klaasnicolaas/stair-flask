"""Initialize Stair Challenge app."""
import random, json
from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from app.mqtt_controller import MQTTClient
from app.led_controller import LEDController
from rpi_ws281x import Color
from app.const import MQTT_TRIGGER_TOPIC, MQTT_STATUS_TOPIC
from app.config import Config

app = Flask(__name__)

# Load config values from app/config.py
app.config.from_object(Config)

# Database configuration
db = SQLAlchemy(app)

# Initialize MQTT client
mqtt = MQTTClient()
mqtt.connect()

# ----------------------------------------------------------------------------#
# LED strip configuration.
# ----------------------------------------------------------------------------#
LED_COUNT = 104       # Number of LED pixels.
LED_PIN = 10          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

led_controller = LEDController(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL)
led_controller.turn_off()

# Install the blueprints
from app.blueprints.backend import bp as backend_bp
from app.blueprints.backend.models import Sensor
app.register_blueprint(backend_bp)

# MQTT callback functions
def on_topic_trigger(client, userdata, message):
    # led_controller.set_color(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    print(f"Message Received from Others: {message.payload.decode()}")

def on_topic_status(client, userdata, message):
    """Callback function for status messages.

    Args:
        client: The client instance for this callback.
        userdata: The private user data as set in Client() or userdata_set().
        message: An instance of MQTTMessage.
    """
    try:
        data = json.loads(message.payload)
        with app.app_context():
            sensor = Sensor.query.filter_by(client_id=data['client_id']).first()
            if sensor:
                # If the sensor already exists
                print(f"Updating sensor: {data['client_id']}")
                sensor.ip_address = data['ip_address']
                sensor.status = data['status']
                sensor.last_update = datetime.now()
                db.session.commit()
            else:
                # If the sensor doesn't exist
                print(f"Adding new sensor: {data['client_id']}")
                sensor = Sensor(client_id=data['client_id'], ip_address=data['ip_address'], status=data['status'], last_update=datetime.now())
                db.session.add(sensor)
                db.session.commit()
    except exc.IntegrityError:
        with app.app_context():
            db.session.rollback()
        print("An error occurred during database operation.")

mqtt.client.message_callback_add(MQTT_TRIGGER_TOPIC, on_topic_trigger)
mqtt.client.message_callback_add(MQTT_STATUS_TOPIC, on_topic_status)

# Create the database tables
with app.app_context():
    print('Creating database tables...')
    db.create_all()

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_color', methods=['GET'])
def set_color():
    args = request.args
    led_controller.set_color(Color(int(args.get('red')), int(args.get('green')), int(args.get('blue'))))
    return redirect('/')

@app.route('/turn_off')
def turn_off():
    led_controller.turn_off()
    return redirect('/')