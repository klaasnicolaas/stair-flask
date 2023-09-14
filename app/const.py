"""Constants for the Stair Challenge app."""
from typing import Final

MQTT_BROKER_HOST: Final = "localhost"
MQTT_BROKER_PORT: int = 1883
MQTT_BROKER_KEEPALIVE: int = 60

MQTT_TEST_TOPIC: Final = "test"
MQTT_TRIGGER_TOPIC: Final = "sensor/+/trigger"