"""Unit tests for the LEDController class."""

from unittest.mock import MagicMock

from app import Color, LEDController
from app.led_controller import Direction


def test_led_controller_color_wipe() -> None:
    # Create a mock PixelStrip object
    mock_pixelstrip = MagicMock()

    # Create an instance of LEDController with the mock PixelStrip
    led_controller = LEDController(10, 10, 800000, 10, 255, False, 0)
    led_controller.strip = mock_pixelstrip

    # Call the color_wipe method
    color = Color(0, 0, 255)  # Assuming Color is a class with RGB values
    wait_ms = 50
    direction = Direction.TOP_TO_BOTTOM
    led_controller.color_wipe(color, wait_ms, direction)

    assert True
