import os
import re

# Escape ansi from stdout
import sys


def is_test(name):
    if len(sys.argv) > 1 and (name in sys.argv):
        return True
    else:
        return False


def app_has_extra_directories(package):
    # remove all directories under /apps
    root_directories = []
    for directory in package["extra_directories"]:
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
