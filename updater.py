from halo import Halo
import os
import sys


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

    print("Get the latest version from https://github.com/dhtdht020/osc-dl/")

    with Halo(text="Checking for updates..", color="yellow", text_color="yellow"):
        check_update()


def check_update():
    print("Automatic updater is not yet implemented.")
