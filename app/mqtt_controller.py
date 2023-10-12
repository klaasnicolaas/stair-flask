"""MQTT Controller Module."""
from __future__ import annotations

import secrets
import socket

import paho.mqtt.client as mqtt

from app.const import MQTT_STATUS_TOPIC, MQTT_TEST_TOPIC, MQTT_TRIGGER_TOPIC
from app.exceptions import StairChallengeConnectionError
from config import Config


# ruff: noqa: ARG002
class MQTTClient:
    """MQTT Client Class."""

    def __init__(self) -> None:
        """Initialize MQTT Client."""
        self.client = mqtt.Client(f"RaspberryPi-{secrets.token_hex(8)}")
        self.client.on_connect = self.on_connect
        # self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

    def on_connect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: dict,  # pylint: disable=unused-argument
        flags: dict,  # pylint: disable=unused-argument
        rc: int,  # pylint: disable=invalid-name
    ) -> None:
        """Define on_publish event function.

        Args:
        ----
            client: The client instance for this callback.
            userdata: The private user data as set in Client() or userdata_set().
            flags: Response flags sent by the broker.
            rc: The connection result.
        """
        if rc == 0:
            print("Connected successfully with MQTT Broker")
            client.subscribe(MQTT_TEST_TOPIC)
            client.subscribe(MQTT_TRIGGER_TOPIC, 1)
            client.subscribe(MQTT_STATUS_TOPIC, 1)
        else:
            print("Connection problem with MQTT Broker!")

    def on_disconnect(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: dict,  # pylint: disable=unused-argument
        rc: int,  # pylint: disable=invalid-name
    ) -> None:
        """Define on_disconnect event function.

        Args:
        ----
            client: The client instance for this callback.
            userdata: The private user data as set in Client() or userdata_set().
            rc: The connection result.
        """
        if rc != 0:
            print("Unexpected disconnection.")

    def on_message(
        self,
        client: mqtt.Client,  # pylint: disable=unused-argument
        userdata: dict,  # pylint: disable=unused-argument
        message: mqtt.MQTTMessage,
    ) -> None:
        """Define on_message event function.

        Args:
        ----
            client: The client instance for this callback.
            userdata: The private user data as set in Client() or userdata_set().
            message: An instance of MQTTMessage.
        """
        print(f"Message Received from Others: {message.payload.decode()}")

    def connect(self) -> None:
        """Connect with MQTT Broker."""
        try:
            self.client.connect(
                Config.MQTT_BROKER_URL,
                Config.MQTT_BROKER_PORT,
                Config.MQTT_KEEPALIVE,
            )
        except (ConnectionRefusedError, socket.gaierror) as exception:
            msg = "Could not connect to MQTT Broker"
            raise StairChallengeConnectionError(
                msg,
            ) from exception

        self.client.loop_start()

    def disconnect(self) -> None:
        """Disconnect from MQTT Broker."""
        self.client.loop_stop()
        self.client.disconnect()

    def send(self, topic: str, payload: str | dict) -> None:
        """Send message to MQTT Broker.

        Args:
        ----
            topic: MQTT topic to send message to.
            payload: Message to send to MQTT Broker.
        """
        self.client.publish(topic, payload)
