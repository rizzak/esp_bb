from my_lib import pcd8544
from machine import Pin, SPI


class Lcd:
    """Display control Nokia 5110"""
    def __init__(self, spi=1, cs=2, dc=15, rst=0, bl=12):
        self.spi = SPI(spi)
        self.cs = Pin(cs)
        self.dc = Pin(dc)
        self.rst = Pin(rst)
        self.bl = bl

        self.spi.init(baudrate=2000000, polarity=0, phase=0)
        self.lcd = pcd8544.PCD8544_FRAMEBUF(self.spi, self.cs, self.dc, self.rst)

    def light(self, status):
        if status == 'on':
            # backlight on
            Pin(self.bl, Pin.OUT, value=0)
        elif status == 'off':
            # backlight off
            Pin(self.bl, Pin.OUT, value=1)

    def text(self, line1='', line2='', line3='', line4='', line5=''):
        # Can show five line of text
        # text(string, x, y, color)
        self.clear()
        self.lcd.text(line1, 0, 0, 1)
        self.lcd.text(line2, 0, 10, 1)
        self.lcd.text(line3, 0, 20, 1)
        self.lcd.text(line4, 0, 30, 1)
        self.lcd.text(line5, 0, 40, 1)
        self.lcd.show()

    def clear(self):
        self.lcd.fill(0)
        self.lcd.show()
