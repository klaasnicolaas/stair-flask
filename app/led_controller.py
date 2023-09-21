"""LED strip module."""
from rpi_ws281x import Color, PixelStrip
import random


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

        Returns:
        ----
            Color: A random color that has not been used yet.
        """
        available_colors = [
            color for color in self.get_all_colors() if color not in self.used_colors
        ]
        if not available_colors:
            available_colors = self.get_all_colors()
            self.used_colors = []

        random.shuffle(available_colors)

        color = random.choice(available_colors)
        self.used_colors.append(color)
        return color

    @classmethod
    def get_all_colors(cls):
        """Return all available colors.

        Returns:
        ----
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
        return random.choice(
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

    def turn_off(self) -> None:
        """Turn off the LED strip."""
        self.set_color(Color(0, 0, 0))
        # print('LED strip turned off')
