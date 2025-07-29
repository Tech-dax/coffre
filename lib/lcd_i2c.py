from machine import I2C, Pin
from lib.i2c_lcd_driver import I2cLcd

I2C_ADDR = 0x27
ROWS = 2
COLUMNS = 16

class LCD:
    def __init__(self, scl=22, sda=21):
        self.i2c = I2C(0, scl=Pin(scl), sda=Pin(sda), freq=400000)
        self.lcd = I2cLcd(self.i2c, I2C_ADDR, ROWS, COLUMNS)
        self.clear()

    def clear(self):
        self.lcd.clear()

    def print(self, text, line=0):
        self.lcd.move_to(0, line)
        self.lcd.putstr(text[:COLUMNS].ljust(COLUMNS))
