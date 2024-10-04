import sys
import requests
import json
from packaging import version

import utils


def current_version():
    major = "1"
    minor = "4"
    patch = "0"

    version_number = f"{major}.{minor}.{patch}"

    # "outofdate": a test meant for checking update-related functions
    if utils.is_test("outofdate"):
        version_number = "1.0.0"

    return version_number


def get_branch():
    return "Stable"


def latest_version():
    return json.loads(requests.get("https://api.github.com/repos/dhtdht020/osc-dl/releases/latest").content)


def is_frozen():
    """Check if frozen with PyInstaller"""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def check_update(updated_version):
    """
    Checks if updated_version is higher than current OSCDL version
    :param updated_version: Dictionary containing information regarding a release from the GitHub API.
    :return: True if higher.
    """
    return version.parse(updated_version["tag_name"]) > version.parse(current_version())
