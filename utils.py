import re

# Escape ansi from stdout
import sys


def is_test(name):
    if len(sys.argv) > 1 and (sys.argv[1] == name):
        return True
    else:
        return False


def is_supported_by_wiiload(package):
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



