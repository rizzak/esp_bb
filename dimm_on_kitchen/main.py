from machine import Pin, PWMfrom time import sleeppin1 = Pin(13, Pin.IN, Pin.PULL_UP)pin2 = Pin(12, Pin.IN, Pin.PULL_UP)pin3 = Pin(14, Pin.IN, Pin.PULL_UP)pin4 = Pin(15, Pin.IN, Pin.PULL_UP)frequency = 120led1 = PWM(Pin(4), frequency)led1.duty(0)led2 = PWM(Pin(5), frequency)led2.duty(0)current_duty = 0off_duty = 0low_duty = 8middle_duty = 128hi_duty = 1024while True:    if pin1.value() == 1:        for i in range(current_duty, off_duty - 1, -1):            if current_duty == off_duty:                break            led1.duty(i)            led2.duty(i)            sleep(0.001)        current_duty = off_duty    elif pin2.value() == 1:        for i in range(current_duty, low_duty, -1 if current_duty > low_duty else 1):            if current_duty == low_duty:                break            led1.duty(i)            led2.duty(i)            sleep(0.001)        current_duty = low_duty    elif pin3.value() == 1:        for i in range(current_duty, middle_duty, -1 if current_duty > middle_duty else 1):            if current_duty == middle_duty:                break            led1.duty(i)            led2.duty(i)            sleep(0.001)        current_duty = middle_duty    elif pin4.value() == 1:        for i in range(current_duty, hi_duty, -1 if current_duty > hi_duty else 1):            if current_duty == hi_duty:                break            led1.duty(i)            led2.duty(i)            sleep(0.001)        current_duty = hi_duty