"""Unit tests for the LEDController class."""

from unittest.mock import MagicMock, patch

from app.led_controller import Color, Direction, LEDController


def test_led_controller_color_wipe(mock_strip: MagicMock) -> None:
    """Test the color_wipe method of the LEDController class.

    Args:
    ----
        mock_strip (MagicMock): The mocked LED strip.
    """
    controller = LEDController(
        count=mock_strip.numPixels(),
        pin=18,
        freq_hz=800000,
        dma=10,
        invert=False,
        brightness=255,
        channel=0,
    )
    controller.start()

    color = Color(0, 255, 0)
    controller.color_wipe(color, wait_ms=50, direction=Direction.BOTTOM_TO_TOP)

    assert mock_strip.setPixelColor.call_count == 10
    assert mock_strip.show.call_count == 10


def test_led_controller_one_led(mock_strip: MagicMock) -> None:
    """Test the one_led method of the LEDController class.

    Args:
    ----
        mock_strip (MagicMock): The mocked LED strip.
    """
    # Arrange
    controller = LEDController(
        count=mock_strip.numPixels(),
        pin=18,
        freq_hz=800000,
        dma=10,
        invert=False,
        brightness=255,
        channel=0,
    )
    controller.start()

    # Act
    color = Color(255, 0, 0)
    led_number = 5
    controller.one_led(color, led_number)

    # Assert
    assert mock_strip.setPixelColor.call_count == 1


# def test_led_controller_rainbow(mock_strip: MagicMock) -> None:
#     """Test the rainbow method of the LEDController class.

#     Args:
#     -----
#         mock_strip (MagicMock): The mocked LED strip.
#     """
#     # Arrange
#     controller = LEDController(
#         count=mock_strip.numPixels(),
#         pin=18,
#         freq_hz=800000,
#         dma=10,
#         invert=False,
#         brightness=255,
#         channel=0,
#     )
#     controller.start()

#     # Act
#     controller.rainbow(wait_ms=20, iterations=1)

#     # Assert
#     assert mock_strip.setPixelColor.call_count == 2560


def test_led_controller_set_sensor_led(mock_strip: MagicMock) -> None:
    """Test the set_sensor_led method of the LEDController class.

    Args:
    ----
        mock_strip (MagicMock): The mocked LED strip.
    """
    # Arrange
    controller = LEDController(
        count=mock_strip.numPixels(),
        pin=18,
        freq_hz=800000,
        dma=10,
        brightness=255,
        invert=False,
        channel=1,
    )
    controller.start()

    # Act
    color = Color(0, 255, 0)

    # Test for an invalid Sensor ID
    invalid_sensor_id = 10
    with patch("builtins.print") as mock_print:
        controller.set_sensor_led(color, invalid_sensor_id)
        mock_print.assert_called_once_with(f"Invalid sensor ID: {invalid_sensor_id}")


def test_led_controller_ripple_effect(mock_strip: MagicMock):
    """Test the ripple_effect method of the LEDController class.

    Args:
    ----
        mock_strip (MagicMock): The mocked LED strip.
    """
    controller = LEDController(
        count=mock_strip.numPixels(),
        pin=18,
        freq_hz=800000,
        dma=10,
        brightness=255,
        invert=False,
        channel=1,
    )
    controller.start()

    start_position = 5
    ripple_length = 3
    color = Color(255, 0, 0)
    wait_ms = 10

    controller.ripple_effect(start_position, ripple_length, color, wait_ms)

    assert mock_strip.setPixelColor.call_count == 2 * ripple_length * 2  # Both directions on and off
    assert mock_strip.show.call_count == 2 * ripple_length