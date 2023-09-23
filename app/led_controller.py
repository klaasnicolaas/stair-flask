"""LED strip module."""
import secrets
import time
from enum import Enum

from rpi_ws281x import Color, PixelStrip


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

        secrets.shuffle(available_colors)

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
        except Exception as e:
            print(f"Error initializing LED strip: {e!s}")

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
            direction (bool): direction of the color wipe - True = top to bottom, False = bottom to top
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
        self.strip.setPixelColor(led + 1, color)
        self.strip.show()

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

    def turn_off(self) -> None:
        """Turn off the LED strip."""
        self.set_color(Color(0, 0, 0))
        # print('LED strip turned off')
