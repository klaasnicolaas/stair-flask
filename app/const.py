"""Constants for the Stair Challenge app."""
# ruff: noqa: E501
import threading
from enum import Enum
from typing import Final

MQTT_SENSOR: Final = "sensor"
MQTT_WORKOUT: Final = "workout"

THREAD_STOP_EVENT = threading.Event()

# MQTT topics - Subscribed
MQTT_TEST_TOPIC: Final = "test"
MQTT_TRIGGER_TOPIC: Final = f"{MQTT_SENSOR}/+/trigger"
MQTT_STATUS_TOPIC: Final = f"{MQTT_SENSOR}/+/status"

# MQTT topics - Published
MQTT_RESTART_ALL_TOPIC: Final = f"{MQTT_SENSOR}/restart_all"
MQTT_WORKOUT_CONTROL_ALL_TOPIC: Final = f"{MQTT_WORKOUT}/control_all"


# Enum classes
class Direction(Enum):
    """Enum for the direction."""

    TOP_TO_BOTTOM = True
    BOTTOM_TO_TOP = False


class SensorLed(Enum):
    """Enum for the sensor LEDs."""

    SENSOR_3: tuple = {"start": 56, "end": 59}
    SENSOR_4: tuple = {"start": 36, "end": 39}
    SENSOR_5: tuple = {"start": 16, "end": 19}
    SENSOR_6: tuple = {"start": 0, "end": 3}


class IsAdmin(Enum):
    """Enum for the admin status."""

    YES = True
    NO = False


class ResetCounter(Enum):
    """Enum for the reset counter."""

    YES = True
    NO = False


WORKOUTS = [
    {
        "name": "Kameleon",
        "description": "Laat de trap van kleur veranderen, tijdens het traplopen.",
        "pros": {"pro1": "Rustige oefening", "pro2": "Open eigen tempo"},
    },
    {
        "name": "Traploop test",
        "description": "Probeer in een beperkte tijd zoveel mogelijk op en neer te gaan.",
        "pros": {
            "pro1": "Conditioneel uitdagend",
            "pro2": "Competitief",
            "pro3": "Tijdsgebonden",
        },
    },
    {
        "name": "Meeloper",
        "description": "Bij elke stap die je zet, zal de LED verlichting jouw tempo volgen.",
        "pros": {"pro1": "Rustige oefening", "pro2": "Open eigen tempo"},
    },
]
