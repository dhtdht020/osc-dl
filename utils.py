import os
import re

# Escape ansi from stdout
import sys
from datetime import datetime


def is_test(name):
    if len(sys.argv) > 1 and (name in sys.argv):
        return True
    else:
        return False


def app_has_extra_directories(package):
    # remove all directories under /apps
    root_directories = []
    for directory in package["subdirectories"]:
        if "/apps" in directory:
            pass
        else:
            root_directories.append(directory)

    if len(root_directories) > 0:
        return False
    else:
        return True


# Get resource when frozen with PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# Returns readable file size from file length
def file_size(length):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(length) < 1024.0:
            return "%3.1f%s%s" % (length, unit, "B")
        length /= 1024.0

    return "%.1f%s%s" % (length, 'Yi', "B")


# Returns mount point for a path in a given device
def get_mount_point(path):
    path = os.path.abspath(path)

    while not os.path.ismount(path):
        path = os.path.dirname(path)

    return path

# check if the app has a birthday
def app_birthday_string(app):
    if datetime.fromtimestamp(int(app["release_date"])).strftime('%m%d') == datetime.now().strftime('%m%d'):
        # verify that it was not added today
        if datetime.fromtimestamp(int(app["release_date"])).strftime('%Y%m%d') != datetime.now().strftime('%Y%m%d'):
            # determine app age
            age = int((datetime.now().timestamp() - int(app["release_date"])) / 31536000)

            # determine st/nd/rd/th
            if age % 10 == 1 and age % 100 != 11:
                age = str(age) + "st"
            elif age % 10 == 2 and age % 100 != 12:
                age = str(age) + "nd"
            elif age % 10 == 3 and age % 100 != 13:
                age = str(age) + "rd"
            else:
                age = str(age) + "th"

            return f"Happy {age} Birthday!"
    return None
