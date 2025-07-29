from machine import Pin, PWM
import time

class Buzzer:
    def __init__(self, pin=15):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty(0)

    def beep(self, duration=0.1):
        self.buzzer.freq(1000)
        self.buzzer.duty(512)
        time.sleep(duration)
        self.buzzer.duty(0)

    def alarm(self, t=2):
        for _ in range(t):
            self.beep(0.2)
            time.sleep(0.2)
