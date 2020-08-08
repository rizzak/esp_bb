from machine import Pin, PWM


class Motor():
    def __init__(self, pin_left_forward=25, pin_left_backward=26, pin_right_forward=32, pin_right_backward=33):
        frequency = 100
        # Motors left side
        self.left_forward = PWM(Pin(pin_left_forward, Pin.OUT), frequency)
        self.left_backward = PWM(Pin(pin_left_backward, Pin.OUT), frequency)
        # Motors right side
        self.right_forward = PWM(Pin(pin_right_forward, Pin.OUT), frequency)
        self.right_backward = PWM(Pin(pin_right_backward, Pin.OUT), frequency)
        self.default_speed = 512

    def move(self, left=500, right=500):
        if left > 0:
            self.left_backward.duty(0)
            self.left_forward.duty(left)
        else:
            self.left_backward.duty(-left)
            self.left_forward.duty(0)

        if right > 0:
            self.right_backward.duty(0)
            self.right_forward.duty(right)
        else:
            self.right_backward.duty(-right)
            self.right_forward.duty(0)

    def forward(self, left=500, right=500):
        self.left_backward.duty(0)
        self.right_backward.duty(0)
        self.left_forward.duty(left)
        self.right_forward.duty(right)

    def reverse(self, left=500, right=500):
        self.left_forward.duty(0)
        self.right_forward.duty(0)
        self.left_backward.duty(left)
        self.right_backward.duty(right)

    def left(self, left=500, right=500):
        self.left_forward.duty(0)
        self.right_forward.duty(right)
        self.left_backward.duty(left)
        self.right_backward.duty(0)

    def right(self, left=500, right=500):
        self.left_forward.duty(left)
        self.right_forward.duty(0)
        self.left_backward.duty(0)
        self.right_backward.duty(right)

    def stop(self):
        self.left_forward.duty(0)
        self.right_forward.duty(0)
        self.left_backward.duty(0)
        self.right_backward.duty(0)
        print("stop")
