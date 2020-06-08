import sys
import requests
import platform
import json
from packaging import version


def current_version():
    beta_number = "6"
    version = "1.2." + beta_number
    return version


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

    check_update()


def check_update():
    latest = latest_version()
    current = current_version()
    if version.parse(latest) > version.parse(current_version()):
        print("OUT OF DATE")
    else:
        print("You are up to date.")
        print("Latest released version: " + latest)
        print("Current version: " + current)


def get_update():
    if is_frozen() is True and platform.system() == 'Windows':
        print('Checking updates for Windows NT, with PyInstaller EXE.')

    if is_frozen() is False and platform.system() == 'Windows':
        print('Checking updates for Windows NT, as script.')
        latest_version()
        update_win32_script()

    if is_frozen() is True and platform.system() == 'Linux':
        print('Checking updates for Linux, with PyInstaller binary.')

    if is_frozen() is False and platform.system() == 'Linux':
        print('Checking updates for Linux, as script.')

    if is_frozen() is True and platform.system() == 'Darwin':
        print('Checking updates for Mac, with PyInstaller binary.')

    if is_frozen() is False and platform.system() == 'Darwin':
        print('Checking updates for Mac, as script.')

    print("\nAutomatic updater for your operating system, version, or executable is not yet implemented.")


def update_win32_script():
    print('oop')
