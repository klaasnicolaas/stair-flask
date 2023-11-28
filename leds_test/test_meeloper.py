import argparse
import time
from enum import Enum

from rpi_ws281x import Color, PixelStrip

CLEAR = False

# LED strip configuration:
LED_COUNT = 104  # Number of LED pixels.
LED_PIN = 10  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
)
# Intialize the library (must be called once before other functions).
strip.begin()


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50, direction=1):
    """Wipe color across display a pixel at a time."""
    num_pixels = strip.numPixels()
    if direction == 1:
        range_start, range_end, range_step = 0, num_pixels, 1
    else:
        range_start, range_end, range_step = num_pixels - 1, -1, -1
    for i in range(range_start, range_end, range_step):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


class Colors(Enum):
    BLACK = Color(0, 0, 0)
    RED = Color(255, 0, 0)
    GREEN = Color(0, 255, 0)
    BLUE = Color(0, 0, 255)


def fill(strip, start, end, color, direction=1, wait_ms=50):
    """Fill LEDs in the specified range with the given color."""
    num_pixels = strip.numPixels()

    if direction == 1:
        range_start, range_end, range_step = start, end + 1, 1
    else:
        range_start, range_end, range_step = end, start - 1, -1

    for i in range(range_start, range_end, range_step):
        strip.setPixelColor(i % num_pixels, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


# Main program logic follows:
if __name__ == "__main__":
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--clear",
        action="store_true",
        help="clear the display on exit",
    )
    args = parser.parse_args()

    print("Press Ctrl-C to quit.")
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        colorWipe(strip, Color(0, 0, 0), 10)
        last_position = 0
        while True:
            if CLEAR:
                colorWipe(strip, Color(0, 0, 0), 10)
                time.sleep(5000)
            else:
                start_trede = int(input("Voer het startnummer van de trede in: "))
                end_trede = int(input("Voer het eindnummer van de trede in: "))
                color = Colors.RED.value  # Hier kun je de gewenste kleur instellen

                fill(strip, start_trede, end_trede, color, -1)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
