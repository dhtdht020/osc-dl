import os
import re
from datetime import datetime

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
    return os.path.join(os.path.abspath("."), relative_path)


# Returns readable file size from file length
def file_size(length):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(length) < 1024.0:
            return "%3.1f%s%s" % (length, unit, "B")
        length /= 1024.0

    return "%.1f%s%s" % (length, 'Yi', "B")

# Returns package badges, from https://github.com/OpenShopChannel/Website/blob/master/utils.py
def application_badges(package):
    badges = {}
    if "wwwwgcnsk" in package["controllers"]:
        badges["all-peripherals"] = ["All Peripherals","Given to applications which support every single peripheral Open Shop Channel keeps track of, with the exception of Wii Zapper, which is not included in any application."]

    if package["short_description"] == "":
        badges["needs-no-description"] = ["Needs no description", "Given to applications which lack a description."]

    # check if added in the past 30 days
    if datetime.now().timestamp() - int(package["release_date"]) < 2592000:
        badges["recently-updated"] = ["Recently Updated", "Given to applications which were added or updated in the last 30 days."]

    # check if zipped app size is over 100MiB
    if int(package["zip_size"]) >= 104857600:
        badges["expensive-delivery"] = ["Expensive Delivery", "Given to applications where the compressed download is over 100MiB."]

    # check if extracted app size is under 500KiB
    if int(package["zip_size"]) <= 512000:
        badges["free-delivery"] = ["Free Delivery", "Given to applications where the compressed download is under 500KiB."]

    # check if the app has a birthday
    if datetime.fromtimestamp(int(package["release_date"])).strftime('%m%d') == datetime.now().strftime('%m%d'):
        # verify that it was not added today
        if datetime.fromtimestamp(int(package["release_date"])).strftime('%Y%m%d') != datetime.now().strftime('%Y%m%d'):
            # determine app age
            age = int((datetime.now().timestamp() - int(package["release_date"])) / 31536000)

            # determine st/nd/rd/th
            if age % 10 == 1 and age % 100 != 11:
                age = str(age) + "st"
            elif age % 10 == 2 and age % 100 != 12:
                age = str(age) + "nd"
            elif age % 10 == 3 and age % 100 != 13:
                age = str(age) + "rd"
            else:
                age = str(age) + "th"
            badges["birthday-app"] = [f"Happy {age} Birthday!", None]

    return badges
