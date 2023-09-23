"""Constants for the Stair Challenge app."""
# ruff: noqa: E501
from typing import Final

MQTT_SENSOR: Final = "sensor"
MQTT_WORKOUT: Final = "workout"

# MQTT topics - Subscribed
MQTT_TEST_TOPIC: Final = "test"
MQTT_TRIGGER_TOPIC: Final = f"{MQTT_SENSOR}/+/trigger"
MQTT_STATUS_TOPIC: Final = f"{MQTT_SENSOR}/+/status"

# MQTT topics - Published
MQTT_RESTART_ALL_TOPIC: Final = f"{MQTT_SENSOR}/restart_all"
MQTT_WORKOUT_CONTROL_ALL_TOPIC: Final = f"{MQTT_WORKOUT}/control_all"

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
