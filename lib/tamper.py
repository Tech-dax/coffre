from machine import Pin

class Tamper:
    def __init__(self, pin=23):
        self.sensor = Pin(pin, Pin.IN)

    def check(self):
        return self.sensor.value() == 1
