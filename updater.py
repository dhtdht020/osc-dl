import sys
import requests
import platform
import json
import yaml
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


def get_type():
    return f'System: {platform.system()}, Frozen: {is_frozen()}'


# Get announcement banner from the announcements repo
def get_announcement():
    # todo complete rewrite
    yaml_file = requests.get("https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/announcement"
                             "/alert.yml").text
    parsed_yaml = yaml.load(yaml_file, Loader=yaml.FullLoader)

    # Get announcement
    announcement_header = parsed_yaml["information"]["header"]
    announcement_content = parsed_yaml["information"]["content"]
    announcement_banner_color = parsed_yaml["information"]["banner"]["color"]
    announcement_banner_text_color = parsed_yaml["information"]["banner"]["text_color"]
    announcement_website_enabled = parsed_yaml["website"]["display"]
    announcement_website_label_text = parsed_yaml["website"]["label"]["text"]
    announcement_website_label_color = parsed_yaml["website"]["label"]["color"]
    announcement_website_url = parsed_yaml["website"]["url"]

    if not parsed_yaml["information"]["display"]:
        return
    # Check YAML version for compatibility, Shows warning on other versions

    announcement = f'<html><head/><body><p><span style=" font-weight:600;">{announcement_header} ' \
                   f'</span>{announcement_content}'

    announcement_url = f'<html><head/><body><p><a href="{announcement_website_url}">' \
                       f'<span style=" text-decoration: underline; color:{announcement_website_label_color};">' \
                       f'{announcement_website_label_text}</span></a></p></body></html>'

    return announcement, announcement_url, announcement_banner_color, announcement_banner_text_color, announcement_website_enabled

