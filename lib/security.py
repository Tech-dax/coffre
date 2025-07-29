class Security:
    def __init__(self, storage, cloud, lcd, buzzer):
        self.storage = storage
        self.cloud = cloud
        self.lcd = lcd
        self.buzzer = buzzer

    def validate_access(self, pwd):
        return pwd == self.storage.get_password()
s