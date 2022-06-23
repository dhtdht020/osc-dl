import json
import requests


class Hosts:
    def __init__(self):
        self.__hosts = None
        self.update()

    def update(self):
        response = json.loads(requests.get(f"https://api.oscwii.org/v2/hosts", timeout=10).text)
        self.__hosts = response["repositories"]

    def list(self):
        return self.__hosts

    def get(self, name):
        return self.__hosts[name]
