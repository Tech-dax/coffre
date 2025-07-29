from machine import Pin
import time

class Keypad:
    def __init__(self, rows=[19, 18, 5, 17], cols=[16, 4, 0]):
        self.rows = [Pin(pin, Pin.OUT) for pin in rows]
        self.cols = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in cols]
        self.keys = [
            ["1","2","3"],
            ["4","5","6"],
            ["7","8","9"],
            ["*","0","#"]
        ]

    def get_key(self):
        for i, row in enumerate(self.rows):
            row.value(1)
            for j, col in enumerate(self.cols):
                if col.value() == 1:
                    while col.value() == 1:
                        time.sleep_ms(10)
                    row.value(0)
                    return self.keys[i][j]
            row.value(0)
        return None
