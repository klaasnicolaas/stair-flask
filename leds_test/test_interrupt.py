import threading
import time

from rpi_ws281x import Color, PixelStrip

# Configure the LED strip
LED_COUNT = 104  # Number of LED pixels.
LED_PIN = 10  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, stop_event, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    while not stop_event.is_set():
        for j in range(256 * iterations):
            if stop_event.is_set():
                break
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)


def set_color(color: Color) -> None:
    """Set the color of the LED strip.

    Args:
    ----
        color (Color): Color object with RGB values
    """
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    # print(f"LED strip set to {color}")


def turn_off() -> None:
    """Turn off the LED strip."""
    set_color(Color(0, 0, 0))
    # print('LED strip turned off')


# Hoofdprogramma
if __name__ == "__main__":
    # Initialisatie van de LED-strip
    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    strip.begin()

    # Maak een stop-event voor de thread
    stop_event = threading.Event()

    # Start de thread voor het rainbow-effect
    rainbow_thread = threading.Thread(target=rainbow, args=(strip, stop_event))
    rainbow_thread.start()

    try:
        # Wacht op een toetsaanslag om het effect te stoppen
        input("Druk op Enter om het rainbow-effect te stoppen...")
        stop_event.set()  # Stel het stop-event in om de thread te stoppen
        rainbow_thread.join()  # Wacht tot de thread is voltooid
        turn_off()  # Zet alle LEDs uit
        strip.show()  # Update de LED-strip
    except KeyboardInterrupt:
        pass  # Als de gebruiker Ctrl+C indrukt, stop dan netjes
