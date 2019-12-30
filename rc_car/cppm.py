# from https://github.com/dhylands/upy-examples/blob/master/ic_test.py
import time

import machine as pyb
import micropython


class Channel(object):
    """
    Interface to a radio channel. Makes working with it a little easier.
    """
    def __init__(self):
        self.pulse_width = 1500
        # calibrations
        self.pulse_min = 640
        self.pulse_max = 2420
        self.pulse_centre = 1500
        self.pulse_angle_90 = 2470
        self.pulse_speed_100 = 2200

    def angle(self):
        """
        return an angle based on the pulse_width.
        """
        return (self.pulse_width - self.pulse_centre) * 90 / self.pulse_angle_90

    def speed(self):
        """
        return a speed based on the pulse_width.
        """
        return (self.pulse_width - self.pulse_centre) * 100 / self.pulse_speed_100

    def percent(self):
        """
        return a value where pulse_min is -100, pulse_centre is 0, and pulse_max is 100
        """
        if self.switch():
            return 100 * (self.pulse_width - self.pulse_centre) / (self.pulse_max - self.pulse_centre)
        else:
            return 100 * (self.pulse_width - self.pulse_centre) / (self.pulse_centre - self.pulse_min)

    def switch(self):
        """
        return True if the signal is greater than the middle position, False otherwise
        """
        return self.pulse_width > self.pulse_centre

    def calibration(self, *args):
        """
        If used with no arguments, receive the calibration in this order:
            (pulse_min, pulse_max, pulse_center, pulse_angle_90, pulse_speed_100)
        If used with arguments, use either 3 or 5 arguments to set the calibration:
            [pulse_min, pulse_max, pulse_centre [, pulse_angle_90, pulse_speed_100]]
        """
        if len(args) == 0:
            return (self.pulse_min, self.pulse_max, self.pulse_centre, self.pulse_angle_90, self.pulse_speed_100)
        if len(args) == 3 or len(args) == 5:
            self.pulse_min = int(args[0])
            self.pulse_max = int(args[1])
            self.pulse_centre = int(args[2])
            if len(args) == 5:
                self.pulse_angle_90 = int(args[3])
                self.pulse_speed_100 = int(args[4])
        else:
            raise TypeError("calibration expecting 1, 4, or 6 arguments, got %d" % (1 + len(args)))


class Ppm(Channel):
    """
    Read pulses from a particular pin.

    @note, this uses timer 2.
    """
    timer = None
    def __init__(self, pin, servo = None):
        """
        :pin: ex pyb.Pin.board.X4, the pin the input is connected to.
        :servo: ex pyb.Servo(1) a servo to control directly from the interrupt.
        """
        self.pin = pin
        if Ppm.timer is None:
            Ppm.timer = pyb.Timer(2, prescaler=83, period=0x0fffffff)
        self.interrupt = Ppm.timer.channel(4, pyb.Timer.IC, pin=pin, polarity=pyb.Timer.BOTH)
        self.start = 0
        self.servo = servo
        self.interrupt.callback(self.callback)

    def callback(self, tim):
        if self.pin.value():
            self.start = self.interrupt.capture()
        else:
            self.pulse_width = self.interrupt.capture() - self.start & 0x0fffffff
            if self.servo:
                self.servo.pulse_width(self.pulse_width)

    def demo():
        # This example requires a servo on X1 and a signal (from a radio) on X4.
        micropython.alloc_emergency_exception_buf(100)

        in_ppm = Ppm(pyb.Pin(3))

        while True:
            # wait forever
            pyb.delay(200)
            print("%d%% %d deg %d speed (%s) %d us" % (in_ppm.percent(), in_ppm.angle(), in_ppm.speed(), "True" if in_ppm.switch() else "False", in_ppm.pulse_width))


class Cppm(object):
    """
    Read a combined PPM signal from a R/C radio.

    @note, this uses timer 2.
    """
    timer = None
    def __init__(self, pin, numChannels = 8, servo = None):
        """
        :pin: ex pyb.Pin.board.X4, the pin the input is connected to.
        :servo: ex pyb.Servo(1) a servo to control directly from the interrupt.
        """
        self.pin = pin
        if Ppm.timer is None:
            Ppm.timer = pyb.Timer(2, prescaler=83, period=0x0fffffff)
        self.interrupt = Ppm.timer.channel(4, pyb.Timer.IC, pin=pin, polarity=pyb.Timer.RISING)
        self.start = 0
        self.width = 0
        self.channel = 0
        self.numChannels = numChannels
        self.ch = []
        for ch in range(numChannels):
            self.ch.append(Channel())
        self.sync_width = 0
        self.frame_count = 0
        self.servo = servo
        self.calibrating = False
        self.interrupt.callback(self.callback)

    def callback(self, tim):
        capture = self.interrupt.capture()
        self.width = (capture - self.start) & 0x0fffffff
        self.start = capture
        if self.width > 4000:
            self.channel = 0
            self.sync_width = self.width
            self.frame_count += 1
            return
        if self.channel == self.numChannels:
            return
        self.ch[self.channel].pulse_width = self.width
        if self.width < self.ch[self.channel].pulse_min:
            self.ch[self.channel].pulse_min = self.width
        if self.width > self.ch[self.channel].pulse_max:
            self.ch[self.channel].pulse_max = self.width
        self.channel += 1

        if self.servo:
            if self.channel == 1:
                self.servo.pulse_width(self.width)

    def calibrate(self, value):
        """
        Turn calibration on or off.
        """
        self.calibrating = value
        if value:
            for ch in self.ch:
                ch.calibration(1500, 1500, 1500)


    def demo():
        # This example requires a servo on X1 and a signal (CPPM from a radio) on X4.
        micropython.alloc_emergency_exception_buf(100)

        in_cppm = Cppm(pyb.Pin(3), 8)

        while True:
            # wait forever
            time.sleep_ms(200)
            for i, ch in enumerate(in_cppm.ch):
                print("Channel %d: %d%% %d deg %d speed (%s) %d us %s" % (i, ch.percent(), ch.angle(), ch.speed(), "True" if ch.switch() else "False", ch.pulse_width, str(ch.calibration())))
