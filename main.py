from lib.menu import Menu
from lib.lcd_i2c import LCD
from lib.keypad import Keypad
from lib.storage import Storage
from lib.tamper import Tamper
from lib.buzzer import Buzzer
from lib.cloud import Cloud
import time

# Initialisation des modules
lcd = LCD()
keypad = Keypad()
storage = Storage()
tamper = Tamper()
buzzer = Buzzer()
cloud = Cloud(storage)
menu = Menu(lcd, keypad, storage, tamper, buzzer, cloud)

print("System ready")

while True:
    menu.loop()
    if tamper.check():
        menu.handle_tamper()
    cloud.sync_logs()
    time.sleep(0.1)
