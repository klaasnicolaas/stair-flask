"""LED strip module."""
# ruff: noqa: PLR0913
from __future__ import annotations

import secrets
import time

from rpi_ws281x import Color, PixelStrip

from app.const import THREAD_STOP_EVENT, Direction, SensorLedLocation
from app.exceptions import StairChalllengeInitializationError


class Colors:
    """Class to store colors."""

    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)
    YELLOW = Color(255, 255, 0)
    PURPLE = Color(255, 0, 255)
    CYAN = Color(0, 255, 255)
    ORANGE = Color(255, 165, 0)
    PINK = Color(255, 192, 203)
    BROWN = Color(165, 42, 42)
    WHITE = Color(255, 255, 255)

    def __init__(self) -> None:
        """Initialize the used colors."""
        self.used_colors: list[Color] = []

    def hex_to_rgb(self, hex_color: str) -> Color:
        """Convert a hex color to RGB.

        Args:
        ----
            hex_color (str): Hex color

        Returns:
        -------
            Color: Color object with RGB values
        """
        # Remove the '#' if it's included in the input string
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        # Check if the input is a valid hex color string
        if not all(c in "0123456789ABCDEFabcdef" for c in hex_color):
            msg = "Invalid hex color string"
            raise ValueError(msg)

        # Convert the hex values to integers
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)

        return Color(red, green, blue)

    def get_random_unique_color(self) -> Color:
        """Return a random color that has not been used yet.

        Returns
        -------
            Color: A random color that has not been used yet.
        """
        available_colors = [
            color for color in self.get_all_colors() if color not in self.used_colors
        ]

        if not available_colors:
            self.used_colors = []
            available_colors = [
                color
                for color in self.get_all_colors()
                if color not in self.used_colors
            ]

        color = secrets.choice(available_colors)
        self.used_colors.append(color)
        return color

    @classmethod
    def get_all_colors(cls: object) -> list[Color]:
        """Return all available colors.

        Returns
        -------
            list: A list of all available colors.
        """
        return [
            cls.RED,
            cls.GREEN,
            cls.BLUE,
            cls.YELLOW,
            cls.PURPLE,
            cls.CYAN,
            cls.ORANGE,
            cls.PINK,
            cls.BROWN,
        ]

    def random_color(self) -> Color:
        """Return a random color."""
        return secrets.choice(
            [
                self.RED,
                self.GREEN,
                self.BLUE,
                self.YELLOW,
                self.PURPLE,
                self.CYAN,
                self.ORANGE,
                self.PINK,
                self.BROWN,
            ],
        )


class LEDController:
    """LED strip configuration."""

    strip: PixelStrip

    def __init__(
        self,
        count: int,
        pin: int,
        freq_hz: int,
        dma: int,
        brightness: int,
        invert: bool,  # noqa: FBT001
        channel: int,
    ) -> None:
        """Initialize LED strip.

        Args:
        ----
            led_count (int): Number of LED pixels
            led_pin (int): GPIO pin connected to the pixels (18 uses PWM!)
            led_freq_hz (int): LED signal frequency in hertz (usually 800khz)
            led_dma (int): DMA channel to use for generating signal (try 10)
            led_brightness (int): Set to 0 for darkest and 255 for brightest
            led_invert (bool): True to invert the signal (using level shift)
            led_channel (int): set to '1' for GPIOs 13, 19, 41, 45 or 53
        """
        self.count = count
        self.pin = pin
        self.freq_hz = freq_hz
        self.dma = dma
        self.brightness = brightness
        self.invert = invert
        self.channel = channel

    def start(self) -> None:
        """Initialize the LED strip.

        Raises
        ------
            StairChalllengeInitializationError: If the LED strip cannot be initialized
        """
        self.strip = PixelStrip(
            self.count,
            self.pin,
            self.freq_hz,
            self.dma,
            self.invert,
            self.brightness,
            self.channel,
        )
        try:
            self.strip.begin()
            # self.set_color(Color(0, 0, 0))
            print("LED strip initialized successfully")
        except StairChalllengeInitializationError as error:
            print(f"Error initializing the LED strip: {error!s}")

    def set_color(self, color: Color) -> None:
        """Set the color of the LED strip.

        Args:
        ----
            color (Color): Color object with RGB values
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        # print(f"LED strip set to {color}")

    def wheel(self, pos: int) -> Color:
        """Generate rainbow colors across 0-255 positions.

        Args:
        ----
            pos (int): position in the rainbow

        Returns:
        -------
            Color: Color object with RGB values
        """
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        if pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

    def color_wipe(
        self,
        color: Color,
        wait_ms: int = 50,
        direction: Direction = Direction.TOP_TO_BOTTOM,
    ) -> None:
        """Wipe color across display a pixel at a time.

        Args:
        ----
            color (Color): Color object with RGB values
            wait_ms (int): milliseconds to wait between pixels
            direction (Direction): direction of the color wipe
        """
        num_puxels = self.strip.numPixels()
        if direction == Direction.TOP_TO_BOTTOM:
            range_start, range_end, range_step = 0, num_puxels, 1
        else:
            range_start, range_end, range_step = num_puxels - 1, -1, -1
        for i in range(range_start, range_end, range_step):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow(self, wait_ms: int = 20, iterations: int = 1) -> None:
        """Draw rainbow that fades across all pixels at once.

        Args:
        ----
            wait_ms (int): milliseconds to wait between pixels
            iterations (int): number of iterations
        """
        for j in range(256 * iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(
                    i,
                    self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255),
                )
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def one_led(self, color: Color, led: int) -> None:
        """Set the color of one LED.

        Args:
        ----
            color (Color): Color object with RGB values
            led (int): LED number
        """
        self.strip.setPixelColor(led, color)
        self.strip.show()

    def set_sensor_led(self, color: Color, sensor_id: int) -> None:
        """Set the color of one sensor LED.

        Args:
        ----
            color (Color): Color object with RGB values
            sensor_id (int): Sensor ID
        """
        match sensor_id:
            case 3:
                self.set_led_range(
                    color,
                    SensorLedLocation.SENSOR_3.value["start"],
                    SensorLedLocation.SENSOR_3.value["end"],
                )
            case 4:
                self.set_led_range(
                    color,
                    SensorLedLocation.SENSOR_4.value["start"],
                    SensorLedLocation.SENSOR_4.value["end"],
                )
            case 5:
                self.set_led_range(
                    color,
                    SensorLedLocation.SENSOR_5.value["start"],
                    SensorLedLocation.SENSOR_5.value["end"],
                )
            case 6:
                self.set_led_range(
                    color,
                    SensorLedLocation.SENSOR_6.value["start"],
                    SensorLedLocation.SENSOR_6.value["end"],
                )
            case _:
                print(f"Invalid sensor ID: {sensor_id}")

    def ripple_effect(self, start_position, ripple_length, color, wait_ms=50) -> None:
        """Wipe color across display a pixel at a time.

        Args:
        ----
            start_position: Startpositie van het ripple-effect
            ripple_length: Lengte van het ripple-effect
            color: Kleur van het ripple-effect
            wait_ms: Wachttijd tussen het aansturen van de leds
        """
        num_pixels = self.strip.numPixels()

        for i in range(ripple_length):
            # Bereken de positie van de leds voor het ripple-effect
            left_led = start_position - i
            right_led = start_position + i

            # Zorg ervoor dat de leds binnen de grenzen vallen
            if 0 <= left_led < num_pixels:
                self.strip.setPixelColor(left_led, color)
            if 0 <= right_led < num_pixels:
                self.strip.setPixelColor(right_led, color)

            self.strip.show()
            time.sleep(wait_ms / 1000.0)

        # Wis de pixels na het voltooien van het ripple-effect
        for i in range(ripple_length):
            left_led = start_position - i
            right_led = start_position + i

            if 0 <= left_led < num_pixels:
                self.strip.setPixelColor(left_led, Color(0, 0, 0))
            if 0 <= right_led < num_pixels:
                self.strip.setPixelColor(right_led, Color(0, 0, 0))

            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def set_led_range(self, color: Color, start: int, end: int) -> None:
        """Set the color of a range of LEDs.

        Args:
        ----
            color (Color): Color object with RGB values
            start (int): start LED number
            end (int): end LED number
        """
        for i in range(start, end):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def sandglass(self, duration: int, color: Color) -> None:
        """Display a sandglass animation for a specified duration.

        Args:
        ----
            duration (int): Duration of the sandglass animation in seconds.
            color (Color): Color object with RGB values
        """
        # Reset the stop event
        THREAD_STOP_EVENT.clear()

        num_leds = self.strip.numPixels()
        self.set_color(color)

        # Calculate the time interval for each LED to turn off
        interval_seconds: int = (duration - 1) / num_leds

        # Wait for the first interval
        time.sleep(1)

        for i in range(num_leds):
            remaining_time = duration - (i * interval_seconds)

            if THREAD_STOP_EVENT.is_set():
                print("Force stopping sandglass animation")
                THREAD_STOP_EVENT.clear()
                break

            # Turn off the current LED
            self.one_led(Color(0, 0, 0), i)

            # Turn off the LED after its corresponding time interval
            if remaining_time < 0:
                print("Time is up, stop sandglass animation")
                self.stop_sandglass_thread()
                break

            # Wait for the interval
            time.sleep(interval_seconds)

    def turn_off(self) -> None:
        """Turn off the LED strip."""
        self.set_color(Color(0, 0, 0))
        # print('LED strip turned off')

    def stop_sandglass_thread(self) -> None:
        """Stop the sandglass thread."""
        THREAD_STOP_EVENT.set()

    def reset_stop_event(self) -> None:
        """Reset the stop event."""
        THREAD_STOP_EVENT.clear()
