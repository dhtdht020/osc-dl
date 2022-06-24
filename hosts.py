import json
import requests


class Hosts:
    def __init__(self):
        self.__hosts = None
        self.update()

    def update(self):
        try:
            response = json.loads(requests.get(f"https://api.oscwii.org/v2/hosts", timeout=10).text)
            self.__hosts = response["repositories"]
            for host in self.__hosts:
                self.__hosts[host]["id"] = host
        except Exception as e:
            self.__hosts = {'primary': {'description': 'Could not retrieve hosts from server. '
                                                       f'Using hardcoded repository. (Error: {e})',
                                        'host': 'hbb1.oscwii.org', 'name': 'Open Shop Channel', 'id': 'primary'}}

    def list(self):
        return self.__hosts

    def get(self, name):
        return self.__hosts[name]
