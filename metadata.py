import logging
import re
import requests
import lxml.etree
from utils import resource_path


# Get icon image
def icon(app):
    try:
        request = requests.get(app["icon_url"])
        icon_image = request.content
        # If icon is not there
        if str(request.status_code) != "200":
            icon_image = missing_icon()
    except Exception:
        icon_image = missing_icon()
    return icon_image


def missing_icon():
    with open(resource_path("assets/gui/missing.png"), mode='rb') as file:
        missing_icon_image = file.read()
        file.close()
    return missing_icon_image


# Get long description from an app's meta XML
def long_description(app_name, repo="hbb1.oscwii.org"):
    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # Remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # Remove HTML comments
    xml = re.sub(r'<!--.*?-->', '', xml, flags=re.DOTALL)

    # Parse XML
    try:
        root = lxml.etree.fromstring(xml)
    except Exception as e:
        logging.error(f"[{app_name}] With the intention to load the long description, "
                      f"OSCDL could not parse the application metadata XML. Information:\n{str(e)}")
        return "No description provided"

    return root.find('long_description').text


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
def parse_peripherals(peripherals):
    peripherals_dict = {"wii_remotes": 0, "nunchuk": False, "classic": False, "gamecube": False,
                        "wii_zapper": False, "keyboard": False, "sdhc": False}

    # One day OSCDL will drop support for <3.10 and this will be a switch statement..
    for character in peripherals:
        if character == "w":
            peripherals_dict["wii_remotes"] += 1
        elif character == "n":
            peripherals_dict["nunchuk"] = True
        elif character =="c":
            peripherals_dict["classic"] = True
        elif character == "g":
            peripherals_dict["gamecube"] = True
        if character == "z":
            peripherals_dict["wii_zapper"] = True
        if character == "k":
            peripherals_dict["keyboard"] = True
        if character == "s":
            peripherals_dict["sdhc"] = True

    return peripherals_dict
