from machine import Pin, PWM
import time


class Sound:
    def __init__(self, pin):
        self.pin = pin

    def start(self):
        tempo = 5

        tones = {
            'c': 262,
            'd': 294,
            'e': 330,
            'f': 349,
            'g': 392,
            'a': 440,
            'b': 494,
            'C': 523,
            ' ': 0,
        }

        beeper = PWM(Pin(self.pin, Pin.OUT), freq=440, duty=512)
        melody = 'cdefgabC'
        rhythm = [8, 8, 8, 8, 4, 4, 4, 4]

        for tone, length in zip(melody, rhythm):
            beeper.freq(tones[tone])
            time.sleep(tempo / length)
        beeper.deinit()
