import requests
import yaml


class Hosts:
    hosts_list = []

    # Get list of dictionaries of repositories
    def list(self):
        # Check if list has been already retrieved
        if self.hosts_list:
            return self.hosts_list
        else:
            try:
                yaml_file = requests.get(
                    "https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/announcement"
                    "/repositories.yml").text
                parsed_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)
                repos = parsed_yaml["repos"]
                for i in repos:
                    display_name = parsed_yaml["repositories"][i]["name"]
                    host = parsed_yaml["repositories"][i]["host"]
                    description = parsed_yaml["repositories"][i]["description"]
                    name = i
                    self.hosts_list.append({"display_name": display_name,
                                            "host": host,
                                            "description": description,
                                            "name": name})
                return self.hosts_list
            except Exception:
                print("Error: Couldn't retrieve repository list from the web.")
                return

    # Get repository info by internal name
    def name(self, name):
        # Check if list was not already retrieved
        if not self.hosts_list:
            self.list()

        n = 0
        for i in self.hosts_list:
            if self.hosts_list[n]["name"] == name:
                return self.hosts_list[n]
            else:
                n += 1
        return

    # Get repository info by address
    def url(self, url):
        # Check if list was not already retrieved
        if not self.hosts_list:
            self.list()

            n = 0
            for i in self.hosts_list:
                if self.hosts_list[n]["host"] == url:
                    return self.hosts_list[n]
                else:
                    n += 1
            return
