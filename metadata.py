import logging
import re
import requests
import lxml.etree
from utils import resource_path


# Get icon image
def icon(app):
    try:
        request = requests.get(app["url"]["icon"])
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
