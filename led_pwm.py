from machine import Pin, PWM
from time import sleep


class LedPwm:
    """For PWM control of led"""
    def __init__(self, pin, frequency=5000):
        self.led = PWM(Pin(pin), frequency)
        self.led.duty(1024)

    def blink_duty(self, count, interval, duty):
        """
            Установить яркость
            count: Количество раз
            interval: Интервал в секундах
            duty: Яркость 1024 - мин, 0 - макс
        """
        for i in range(count):
            # Зажигаю светодиод
            self.led.duty(duty)
            sleep(interval)
            # Гашу светодиод
            self.led.duty(1024)
            sleep(interval)
