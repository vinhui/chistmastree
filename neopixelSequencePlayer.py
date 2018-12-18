import config as cfg
from sequencePlayer import SequencePlayer
from neopixel import Adafruit_NeoPixel


class NeopixelSequencePlayer(SequencePlayer):
    def __init__(self):
        super().__init__()

        self.strip = Adafruit_NeoPixel(
            cfg.LED_COUNT,
            cfg.LED_DATA_PIN,
            cfg.LED_FREQ_HZ,
            cfg.LED_DMA,
            cfg.LED_INVERT,
            cfg.LED_BRIGHTNESS,
            cfg.LED_CHANNEL,
            cfg.LED_STRIP)
        self.strip.begin()

    def setrangecolor(self, start, end, color, write=True):
        super().setrangecolor(start, end, color, write)
        if write:
            self.strip.show()

    def setcolor(self, led, color, write=True):
        self.strip.setPixelColor(led, color.topixel())
        if write:
            self.strip.show()
