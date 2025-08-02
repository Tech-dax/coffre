# cloud.py

try:
    import urequests as requests  # MicroPython
except ImportError:
    import requests  # Python standard

class Cloud:
    def __init__(self, storage, server_url):
        self.storage = storage
        self.server_url = server_url

    def is_online(self):
        return self.online
    
    @property
    def online(self):
        response = requests.post(f"{self.server_url}/check")
        if response.status_code == 200:
            return True

    def send_event(self, event_type, data=None):
        if self.is_online():
            payload = {"type": event_type, "data": data}
            try:
                response = requests.post(f"{self.server_url}/event", json=payload)
                if response.status_code == 200:
                    print("[Cloud] Event envoyé avec succès.")
                    return 'ok'
                else:
                    print(f"[Cloud] Échec d’envoi. Code: {response.status_code}")
                    self.storage.add_log(event_type, data)
                    return 'erreur'
            except Exception as e:
                print(f"[Cloud] Erreur d’envoi: {e}")
                self.storage.add_log(event_type, data)
                return None
        else:
            print("[Cloud] Hors ligne, stockage local.")
            self.storage.add_log(event_type, data)
            return 'offline'

    def sync_logs(self):
        if self.is_online():
            logs = self.storage.get_logs()
            if logs:
                try:
                    response = requests.post(f"{self.server_url}/sync", json={"logs": logs})
                    if response.status_code == 200:
                        print("[Cloud] Logs synchronisés.")
                        self.storage.clear_logs()
                    else:
                        print(f"[Cloud] Échec sync. Code: {response.status_code}")
                except Exception as e:
                    print(f"[Cloud] Erreur sync: {e}")
