import json
import os
import sys

import requests
import lxml.etree

GREEN = '\033[92m'
FAIL = '\033[91m'


# Get resource when frozen with PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Get icon of homebrew app. Should be updated to use API sooner or later!
def icon(app_name, repo="hbb1.oscwii.org"):
    try:
        request = requests.get("https://" + repo + "/hbb/" + app_name + ".png")
        icon = request.content
        # If icon is not there
        if str(request.status_code) != "200":
            with open(resource_path("assets/gui/missing.png"), mode='rb') as file:
                icon = file.read()
                file.close()
            # icon = resource_path("assets/gui/missing.png")
    except Exception:
        with open(resource_path("assets/gui/missing.png"), mode='rb') as file:
            icon = file.read()
            file.close()
    return icon


# Get direct download url of app. Should be replaced with API response sooner or later.
def url(app_name, repo="hbb1.oscwii.org"):
    app_url = "https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip"
    return app_url


# Get JSON of specified packages from API
def get_apps(host_name="primary"):
    try:
        json_req = requests.get(f"https://api.oscwii.org/v2/{host_name}/packages", timeout=10)
        if json_req.status_code != 200:
            raise Exception("Cannot reach Open Shop Channel API.")

    except Exception as e:
        # Return fake apps list with offline app
        return json.loads('''
        [{
            "category": "demos", 
            "coder": "-", 
            "contributors": "", 
            "controllers": "", 
            "display_name": "1 : You are not connected to the internet.", 
            "downloads": 0, 
            "extra_directories": [], 
            "extracted": 0, 
            "icon_url": "https://hbb1.oscwii.org/hbb/offline.png", 
            "internal_name": "FakeAppOfflineError", 
            "long_description": "Could not connect to the server. Please check your internet connection.", 
            "package_type": "dol", 
            "rating": "", 
            "release_date": 1557464400, 
            "shop_title_id": "", 
            "shop_title_version": "", 
            "short_description": "Please check your internet connection.", 
            "updated": 1557464400, 
            "version": "1", 
            "zip_size": 0, 
            "zip_url": "https://hbb1.oscwii.org/hbb/offline/offline.zip"
        },
        {
            "category": "demos", 
            "coder": "-", 
            "contributors": "", 
            "controllers": "", 
            "display_name": "2 : The server is potentially down.", 
            "downloads": 0, 
            "extra_directories": [], 
            "extracted": 0, 
            "icon_url": "https://hbb1.oscwii.org/hbb/offline.png", 
            "internal_name": "FakeAppOfflineInfo", 
            "long_description": "OSCWII.ORG is potentially down. Please contact us.", 
            "package_type": "dol", 
            "rating": "", 
            "release_date": 1557464400, 
            "shop_title_id": "", 
            "shop_title_version": "", 
            "short_description": "Please contact us.", 
            "updated": 1557464400, 
            "version": "1", 
            "zip_size": 0, 
            "zip_url": "https://hbb1.oscwii.org/hbb/offline/offline.zip"
        }]''')

    return json.loads(json_req.text)


# Get long description from an app's meta XML
def long_description(app_name, repo="hbb1.oscwii.org"):
    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # Remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # Parse XML
    try:
        root = lxml.etree.fromstring(xml)
    except Exception:
        pass

    try:
        long_description = root.find('long_description').text
    except Exception:
        long_description = "No description provided"

    return long_description


# Returns readable file size from file length
def file_size(length):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(length) < 1024.0:
            return "%3.1f%s%s" % (length, unit, "B")
        length /= 1024.0

    return "%.1f%s%s" % (length, 'Yi', "B")


# Get display name of category with internal name
def category_display_name(category):
    if category == "demos":
        return "Demo"
    elif category == "emulators":
        return "Emulator"
    elif category == "games":
        return "Game"
    elif category == "media":
        return "Media"
    elif category == "utilities":
        return "Utility"
    else:
        return ""


# Parse controllers string
def parse_controllers(controllers):
    wii_remotes = 0
    nunchuk = classic_controller = gamecube_controller = wii_zapper = keyboard = sdhc_compatible = False

    # Wii Remotes
    if "wwww" in controllers:
        wii_remotes = 4
    elif "www" in controllers:
        wii_remotes = 3
    elif "ww" in controllers:
        wii_remotes = 2
    elif "w" in controllers:
        wii_remotes = 1

    # Nunchuk
    if "n" in controllers:
        nunchuk = True

    # Classic Controller
    if "c" in controllers:
        classic_controller = True
    if "g" in controllers:
        gamecube_controller = True
    if "z" in controllers:
        wii_zapper = True
    if "k" in controllers:
        keyboard = True
    if "s" in controllers:
        sdhc_compatible = True

    return wii_remotes, nunchuk, classic_controller, gamecube_controller, wii_zapper, keyboard, sdhc_compatible


# API-related functions
class API:
    host_name = "primary"

    packages = None

    def get_packages(self):
        self.packages = get_apps()

    # Change repository
    def set_host(self, host):
        if host == self.host_name and (self.packages):
            pass
        else:
            self.host_name = host
            self.packages = get_apps(host_name=host)

    # Metadata for given application
    def information(self, internal_name):
        for i in self.packages:
            if i["internal_name"] == internal_name:
                return i
        return
