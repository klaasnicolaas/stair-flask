"""LED strip module."""
from rpi_ws281x import PixelStrip, Color

class LEDController:
    """LED strip configuration"""
    def __init__(self, count, pin, freq_hz, dma, brightness, invert, channel):
        """Initialize LED strip.

        Args:
            led_count (int): Number of LED pixels
            led_pin (int): GPIO pin connected to the pixels (18 uses PWM!)
            led_freq_hz (int): LED signal frequency in hertz (usually 800khz)
            led_dma (int): DMA channel to use for generating signal (try 10)
            led_brightness (int): Set to 0 for darkest and 255 for brightest
            led_invert (bool): True to invert the signal (when using NPN transistor level shift)
            led_channel (int): set to '1' for GPIOs 13, 19, 41, 45 or 53
        """
        self.strip = PixelStrip(count, pin, freq_hz, dma, invert, brightness, channel)
        try:
            self.strip.begin()
            self.set_color(Color(0, 0, 0))
            print('LED strip initialized successfully')
        except Exception as e:
            print(f'Error initializing LED strip: {str(e)}')

    def set_color(self, color):
        """Set the color of the LED strip.

        Args:
            color (Color): Color object with RGB values
        """
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()
        # print(f"LED strip set to {color}")

    def turn_off(self):
        """Turn off the LED strip."""
        self.set_color(Color(0, 0, 0))
        # print('LED strip turned off')
