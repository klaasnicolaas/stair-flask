import argparse
import time

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


# Functie voor het ripple-effect
def ripple_effect(strip, start_position, ripple_length, color, wait_ms=50) -> None:
    """Wipe color across display a pixel at a time.

    Args:
    ----
        strip: NeoPixel object
        start_position: Startpositie van het ripple-effect
        ripple_length: Lengte van het ripple-effect
        color: Kleur van het ripple-effect
        wait_ms: Wachttijd tussen het aansturen van de leds
    """
    num_pixels = strip.numPixels()

    for i in range(ripple_length):
        # Bereken de positie van de leds voor het ripple-effect
        left_led = start_position - i
        right_led = start_position + i

        # Zorg ervoor dat de leds binnen de grenzen vallen
        if 0 <= left_led < num_pixels:
            strip.setPixelColor(left_led, color)
        if 0 <= right_led < num_pixels:
            strip.setPixelColor(right_led, color)

        strip.show()
        time.sleep(wait_ms / 1000.0)

    # Wis de pixels na het voltooien van het ripple-effect
    for i in range(ripple_length):
        left_led = start_position - i
        right_led = start_position + i

        if 0 <= left_led < num_pixels:
            strip.setPixelColor(left_led, Color(0, 0, 0))
        if 0 <= right_led < num_pixels:
            strip.setPixelColor(right_led, Color(0, 0, 0))

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
        # Vraag de gebruiker om de startpositie in te voeren
        end_position = int(input(f"Voer de eindpositie in (0 t/m {LED_COUNT - 1}): "))

        while True:
            if CLEAR:
                colorWipe(strip, Color(0, 0, 0), 10)
                time.sleep(5000)
            else:
                ripple_effect(
                    strip, end_position, ripple_length=10, color=Color(0, 0, 255)
                )

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
