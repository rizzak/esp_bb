import time
import machine


class Blink:
    """For blinking led"""
    def __init__(self, pin):
        self.led = machine.Pin(pin, machine.Pin.OUT)
        self.led.off()

    def blink(self, count, interval):
        """
            Помигать светодиодом
            count: Количество раз
            interval: Интервал в секундах
        """
        for i in range(count):
            # Зажигаю светодиод
            self.led.on()
            time.sleep(interval)
            # Гашу светодиод
            self.led.off()
            time.sleep(interval)
