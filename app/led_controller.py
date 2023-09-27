"""LED strip module."""
import secrets
import threading
import time
from enum import Enum

from rpi_ws281x import Color, PixelStrip

thread_stop_event = threading.Event()


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

    def __init__(self) -> None:
        """Initialize the used colors."""
        self.used_colors = []

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

    def get_random_unique_color(self) -> None:
        """Return a random color that has not been used yet.

        Returns
        -------
            Color: A random color that has not been used yet.
        """
        available_colors = [
            color for color in self.get_all_colors() if color not in self.used_colors
        ]
        if not available_colors:
            available_colors = self.get_all_colors()
            self.used_colors = []

        color = secrets.choice(available_colors)
        self.used_colors.append(color)
        return color

    @classmethod
    def get_all_colors(cls: object) -> list:
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


class StripInvert(Enum):
    """Enum for strip inversion."""

    TRUE = True
    FALSE = False


class SensorLed(Enum):
    """Enum for the sensor LEDs."""

    SENSOR_3 = 58
    SENSOR_4 = 38
    SENSOR_5 = 18
    SENSOR_6 = 0


class LEDController:
    """LED strip configuration."""

    def __init__(
        self,
        count: int,
        pin: int,
        freq_hz: int,
        dma: int,
        brightness: int,
        invert: bool,
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
            led_invert (bool): True to invert the signal (when using level shift)
            led_channel (int): set to '1' for GPIOs 13, 19, 41, 45 or 53
        """
        self.strip = PixelStrip(count, pin, freq_hz, dma, invert, brightness, channel)
        try:
            self.strip.begin()
            # self.set_color(Color(0, 0, 0))
            print("LED strip initialized successfully")
        except Exception as error:
            print(f"Error initializing LED strip: {error!s}")

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
        direction: bool = True,
    ) -> None:
        """Wipe color across display a pixel at a time.

        Args:
        ----
            color (Color): Color object with RGB values
            wait_ms (int): milliseconds to wait between pixels
            direction (bool): direction of the color wipe
                True = top to bottom, False = bottom to top
        """
        num_puxels = self.strip.numPixels()
        if direction:
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
                self.one_led(color, SensorLed.SENSOR_3.value)
            case 4:
                self.one_led(color, SensorLed.SENSOR_4.value)
            case 5:
                self.one_led(color, SensorLed.SENSOR_5.value)
            case 6:
                self.one_led(color, SensorLed.SENSOR_6.value)
            case _:
                print(f"Invalid sensor ID: {sensor_id}")

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
        num_leds = self.strip.numPixels()
        self.set_color(color)

        # Calculate the time interval for each LED to turn off
        interval_seconds: int = (duration - 1) / num_leds

        # Wait for the first interval
        time.sleep(1)

        for i in range(num_leds):
            remaining_time = duration - (i * interval_seconds)

            if thread_stop_event.is_set():
                print("Force stopping sandglass animation")
                thread_stop_event.clear()
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
        thread_stop_event.set()
