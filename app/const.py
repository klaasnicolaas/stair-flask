"""Constants for the Stair Challenge app."""
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
