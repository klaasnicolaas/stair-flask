"""Unit tests for the MQTTClient class."""
from unittest.mock import MagicMock, call, patch

import pytest

from app import MQTTClient
from app.const import MQTT_STATUS_TOPIC, MQTT_TEST_TOPIC, MQTT_TRIGGER_TOPIC
from app.exceptions import StairChallengeMQTTConnectionError


class TestMQTTClient:
    """Test class for the MQTTClient class."""

    @pytest.fixture
    def mqtt_client(self) -> MQTTClient:
        """MQTTClient fixture."""
        return MQTTClient()

    def test_on_connect_success(self, mqtt_client: MQTTClient) -> None:
        """Test that the on_connect method subscribes to the correct topics on successful connection.

        Args:
        ----
            mqtt_client: MQTTClient instance.
        """
        # Mock the necessary objects
        client = MagicMock()
        userdata = {}
        flags = {}
        rc = 0

        # Call the on_connect method
        mqtt_client.on_connect(client, userdata, flags, rc)

        # Assert that the client subscribes to the correct topics on successful connection
        client.subscribe.assert_has_calls(
            [
                call(MQTT_TEST_TOPIC),
                call(MQTT_TRIGGER_TOPIC, 1),
                call(MQTT_STATUS_TOPIC, 1),
            ],
        )

    @patch("paho.mqtt.client.Client.publish")
    def test_send(self, mock_publish: MagicMock, mqtt_client: MQTTClient) -> None:
        """Test that the send method calls the correct method with the correct arguments.

        Args:
        ----
            mock_publish: Mocked publish method.
            mqtt_client: MQTTClient instance.
        """
        # Mock data
        topic = "test_topic"
        payload = "test_payload"

        # Call the send method
        mqtt_client.send(topic, payload)

        # Assert that the publish method is called with the correct arguments
        mock_publish.assert_called_with(topic, payload)

    def test_on_connect_failure(
        self,
        mqtt_client: MQTTClient,
        capsys: pytest.fixture,
    ) -> None:
        """Test that the on_connect method prints the correct error message when the connection fails.

        Args:
        ----
            mqtt_client: MQTTClient instance.
            capsys: Pytest fixture to capture stdout and stderr.
        """
        # Mock the necessary objects
        client = MagicMock()
        userdata = {}
        flags = {}
        rc = 1  # Indicating a connection problem

        # Call the on_connect method
        mqtt_client.on_connect(client, userdata, flags, rc)

        # Assert that the appropriate error message is printed
        captured = capsys.readouterr()
        assert "Connection problem with MQTT Broker!" in captured.out

    @patch("paho.mqtt.client.Client.loop_stop")
    @patch("paho.mqtt.client.Client.disconnect")
    def test_disconnect(
        self,
        mock_disconnect: MagicMock,
        mock_loop_stop: MagicMock,
        mqtt_client: MQTTClient,
    ) -> None:
        """Test that the disconnect method calls the correct methods.

        Args:
        ----
            mock_disconnect: Mocked disconnect method.
            mock_loop_stop: Mocked loop_stop method.
            mqtt_client: MQTTClient instance.
        """
        # Call the disconnect method
        mqtt_client.disconnect()

        # Assert that the loop_stop and disconnect methods are called
        mock_loop_stop.assert_called_once()
        mock_disconnect.assert_called_once()

    def test_on_disconnect_unexpected(
        self,
        mqtt_client: MQTTClient,
        capsys: pytest.fixture,
    ) -> None:
        """Test that the on_disconnect method prints the correct error message when the disconnection is unexpected.

        Args:
        ----
            mqtt_client: MQTTClient instance.
            capsys: Pytest fixture to capture stdout and stderr.
        """
        # Mock the necessary objects
        client = MagicMock()
        userdata = {}
        rc = 1  # Indicating an unexpected disconnection

        # Call the on_disconnect method
        mqtt_client.on_disconnect(client, userdata, rc)

        # Assert that the appropriate error message is printed
        captured = capsys.readouterr()
        assert "Unexpected disconnection." in captured.out

    @patch("paho.mqtt.client.Client.connect")
    def test_connect_successful(
        self,
        mock_connect: MagicMock,
        mqtt_client: MQTTClient,
    ) -> None:
        """Test that the connect method calls the correct method with the correct arguments.

        Args:
        ----
            mock_connect: Mocked connect method.
            mqtt_client: MQTTClient instance.
        """
        # Call the connect method
        mqtt_client.connect("localhost", 1883, 60)

        # Assert that the connect method is called with the correct arguments
        mock_connect.assert_called_with(
            "localhost",
            1883,
            60,
        )

    @patch("paho.mqtt.client.Client.connect", side_effect=ConnectionRefusedError)
    def test_connect_failure(
        self,
        mock_connect: MagicMock,  # noqa: ARG002
        mqtt_client: MQTTClient,
    ) -> None:
        """Test that the connect method raises the correct exception when the connection fails.

        Args:
        ----
            mock_connect: Mocked connect method.
            mqtt_client: MQTTClient instance.
        """
        with pytest.raises(StairChallengeMQTTConnectionError) as e:
            # Call the connect method and assert that it raises the correct exception
            mqtt_client.connect("blabla", 1883, 60)

        # Check if the exception contains the expected message
        assert str(e.value) == "Could not connect to MQTT Broker at blabla."
