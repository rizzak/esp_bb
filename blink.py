import time
import machine


class Blink:
    """For blinking led"""
    def __init__(self, pin):
        self.led = machine.Pin(pin, machine.Pin.OUT)

    def blink(self, count, interval):
        for i in count:
            # Зажигаю светодиод
            self.led.off()
            time.sleep(interval)
            # Гашу светодиод
            self.led.on()
            time.sleep(interval)
