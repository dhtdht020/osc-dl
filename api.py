import json
import requests


class Applications:
    def __init__(self):
        self.__apps = None
        self.update()

    def update(self):
        response = json.loads(requests.get(f"https://hbb1.oscwii.org/api/v3/contents", timeout=10).text)
        self.__apps = response

    def get_apps(self):
        return self.__apps
