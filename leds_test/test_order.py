import time

from rpi_ws281x import *

# LED-strip configuratie
LED_COUNT = 104  # Number of LED pixels.
LED_PIN = 10  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 100  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Deelinstellingen
AANTAL_DELEN = 5
LEDS_PER_DEEL = LED_COUNT // AANTAL_DELEN

# Initialiseer de LED-strip
strip = Adafruit_NeoPixel(
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
)
strip.begin()


# Functie om een deel van de ledstrip aan te sturen
def aansturen_deel(start_led, eind_led, kleur):
    for i in range(start_led, eind_led):
        strip.setPixelColor(i, kleur)
    strip.show()


# Voorbeelddriver met een trigger voor elk deel
def main():
    kleuren = [
        Color(255, 0, 0),  # Rood
        Color(0, 255, 0),  # Groen
        Color(0, 0, 255),  # Blauw
        Color(255, 255, 0),  # Geel
        Color(255, 0, 255),  # Magenta
    ]

    while True:
        # Trigger sequentiëel elk deel
        for deel in range(AANTAL_DELEN):
            start_led = deel * LEDS_PER_DEEL
            eind_led = start_led + LEDS_PER_DEEL

            # Stel de kleur in op basis van het deelnummer
            kleur = kleuren[deel % len(kleuren)]

            aansturen_deel(start_led, eind_led, kleur)
            time.sleep(1)  # Wacht 1 seconde tussen elk deel


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ruim de LED-strip op bij een toetsenbordonderbreking
        strip.clear()
        strip.show()
