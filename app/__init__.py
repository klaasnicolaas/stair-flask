"""Initialize Stair Challenge app."""
import random
from flask import Flask, render_template, request
from app.mqtt_controller import MQTTClient
from app.led_controller import LEDController
from rpi_ws281x import Color
from app.const import MQTT_TRIGGER_TOPIC

app = Flask(__name__)

# Initialize MQTT client
mqtt_client = MQTTClient()
mqtt_client.connect()

# LED strip configuration:
LED_COUNT = 104       # Number of LED pixels.
LED_PIN = 10          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 125  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

led_controller = LEDController(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, LED_CHANNEL)

def on_topic_trigger(client, userdata, message):
    led_controller.set_color(Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    print("Message Received from Others: {}".format(message.payload.decode()))

mqtt_client.client.message_callback_add(MQTT_TRIGGER_TOPIC, on_topic_trigger)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/set_color', methods=['GET'])
def set_color():
    args = request.args
    led_controller.set_color(Color(int(args.get('red')), int(args.get('green')), int(args.get('blue'))))
    return 'Color set'

@app.route('/turn_off')
def turn_off():
    led_controller.turn_off()
    return render_template('index.html')