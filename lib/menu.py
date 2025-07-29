import time
from lib.security import Security
import network

class Menu:
    def __init__(self, lcd, keypad, storage, tamper, buzzer, cloud):
        self.lcd = lcd
        self.keypad = keypad
        self.storage = storage
        self.tamper = tamper
        self.buzzer = buzzer
        self.cloud = cloud
        self.security = Security(storage, cloud, lcd, buzzer)
        self.failed_attempts = 0

    def loop(self):
        self.lcd.clear()
        self.lcd.print("Entrer MDP:")
        pwd = self._read_password()

        if pwd == "*":  # Menu admin
            self.show_admin_menu()
            return

        if pwd:
            if self.cloud.is_online():
                if self.security.validate_access(pwd):
                    self._grant_access(offline=False)
                else:
                    self._deny_access(offline=False)
            else:
                # Offline : seul le mot de passe maître est accepté
                if pwd == self.storage.get_master_password():
                    self._grant_access(offline=True)
                else:
                    self._deny_access(offline=True)

    def _grant_access(self, offline=False):
        self.lcd.clear()
        self.lcd.print("Ouverture...")
        self.buzzer.beep()
        self.failed_attempts = 0
        self.cloud.send_event("open", {"offline": offline})
        self.storage.add_log("open", {"offline": offline})
        time.sleep(1)

    def _deny_access(self, offline=False):
        self.failed_attempts += 1
        self.lcd.clear()
        self.lcd.print("Erreur MDP")
        self.buzzer.alarm(2)
        self.cloud.send_event("wrong_password", {"attempts": self.failed_attempts, "offline": offline})
        self.storage.add_log("wrong_password", {"attempts": self.failed_attempts, "offline": offline})
        if self.failed_attempts >= 3:
            self.handle_tamper()
        time.sleep(1)

    def show_admin_menu(self):
        options = ["Changer MDP", "WiFi", "Reset MDP", "Retour"]
        index = 0

        while True:
            self.lcd.clear()
            self.lcd.print(options[index])
            key = self.keypad.get_key()

            if key == "2":  # Suivant
                index = (index + 1) % len(options)
            elif key == "5":  # Précédent
                index = (index - 1) % len(options)
            elif key == "#":  # Valider
                if options[index] == "Changer MDP":
                    self.change_password()
                elif options[index] == "WiFi":
                    self.scan_wifi()
                elif options[index] == "Reset MDP":
                    self.reset_password()
                elif options[index] == "Retour":
                    break
            time.sleep(0.2)

    def change_password(self):
        self.lcd.clear()
        self.lcd.print("Nouveau MDP:")
        new_pwd = self._read_password(confirm=True)
        if new_pwd:
            self.storage.set_password(new_pwd)
            self.cloud.send_event("password_changed")
            self.storage.add_log("password_changed")
            self.lcd.print("MDP modifie")
            time.sleep(1)

    def reset_password(self):
        self.lcd.clear()
        self.lcd.print("Reset MDP?")
        self.lcd.print("Confirmer #")
        key = self.keypad.get_key()
        if key == "#":
            self.storage.set_password("0000")
            self.cloud.send_event("password_reset")
            self.storage.add_log("password_reset")
            self.lcd.print("MDP = 0000")
            time.sleep(1)

    def scan_wifi(self):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        self.lcd.clear()
        self.lcd.print("Scan WiFi...")
        nets = wlan.scan()
        ssids = [n[0].decode() for n in nets][:5] or ["Aucun"]
        index = 0

        while True:
            self.lcd.clear()
            self.lcd.print(ssids[index])
            key = self.keypad.get_key()

            if key == "2":
                index = (index + 1) % len(ssids)
            elif key == "5":
                index = (index - 1) % len(ssids)
            elif key == "#":
                self.lcd.clear()
                self.lcd.print("MDP WiFi:")
                pwd = self._read_password()
                self.storage.set_wifi(ssids[index], pwd)
                self.cloud.send_event("wifi_set", {"ssid": ssids[index]})
                self.storage.add_log("wifi_set", {"ssid": ssids[index]})
                self.lcd.print("Sauvegarde")
                time.sleep(1)
                break
            elif key == "*":
                break

    def _read_password(self, confirm=False):
        pwd = ""
        while True:
            if self.tamper.check():
                self.handle_tamper()
                return None

            key = self.keypad.get_key()
            if not key:
                continue

            if key == "#":
                if confirm:
                    self.lcd.clear()
                    self.lcd.print("Confirmer:")
                    confirm_pwd = self._read_password()
                    return pwd if confirm_pwd == pwd else None
                return pwd
            elif key == "*":
                if pwd == "":
                    return "*"
                else:
                    pwd = pwd[:-1]
                    self.lcd.clear()
                    self.lcd.print("*" * len(pwd))
            else:
                pwd += key
                self.lcd.clear()
                self.lcd.print("*" * len(pwd))

    def handle_tamper(self):
        self.lcd.clear()
        self.lcd.print("Alerte !")
        self.buzzer.alarm(5)
        self.cloud.send_event("tamper")
        self.storage.add_log("tamper")
