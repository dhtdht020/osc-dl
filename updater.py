import sys
import requests
import platform
import json
import yaml
from packaging import version


def current_version():
    prefix = "1.2."
    beta_number = "8"

    version = prefix + beta_number

    return version


def get_branch():
    branch = "DEV"
    return branch


def latest_version():
    u = requests.get("https://api.github.com/repos/dhtdht020/osc-dl/releases/latest")
    data = json.loads(u.content)
    for key, value in data.items():
        if key == "tag_name":
            return value


def is_frozen():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Packaged with PyInstaller.
        return True
    else:
        # Running in a normal Python script, not packaged by PyInstaller.
        return False


def init_update():
    if is_frozen() is True:
        print('Packaged with PyInstaller.')
    else:
        print('Running in a normal Python script, not packaged by PyInstaller.')

    print("Get the latest version from https://github.com/dhtdht020/osc-dl/\n")

    if check_update() is True:
        print("OSC-DL is out of date.")
        print("Latest released version: " + latest_version())
        print("Current version: " + current_version())
    else:
        print("You are up to date.")
        print("Latest released version: " + latest_version())
        print("Current version: " + current_version())


def check_update():
    latest = latest_version()
    if version.parse(latest) > version.parse(current_version()):
        # out of date
        return True
    else:
        # up to date
        return False


def get_type():
    if is_frozen() is True and platform.system() == 'Windows':
        return 'Windows NT, with PyInstaller EXE.'

    if is_frozen() is False and platform.system() == 'Windows':
        return 'Windows NT, as script.'

    if is_frozen() is True and platform.system() == 'Linux':
        return 'Linux, with PyInstaller binary.'

    if is_frozen() is False and platform.system() == 'Linux':
        return 'Linux, as script.'

    if is_frozen() is True and platform.system() == 'Darwin':
        return 'Mac, with PyInstaller binary.'

    if is_frozen() is False and platform.system() == 'Darwin':
        return 'Mac, as script.'

    return 'Unknown System, Never saw this before. Damn.'


def get_announcement():
    pass
