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

    def move(self, left_forward=222, right_forward=222, left_backward=0, right_backward=0):
        self.left_forward.duty(left_forward)
        self.right_forward.duty(right_forward)
        self.left_backward.duty(left_backward)
        self.right_backward.duty(right_backward)

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
