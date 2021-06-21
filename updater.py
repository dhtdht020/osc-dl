import sys
import requests
import platform
import json
import yaml
from packaging import version


def current_version():
    prefix = "1.2."
    beta_number = "11.1"

    version_number = prefix + beta_number

    return version_number


def get_branch():
    branch = "Stable"
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


# Get announcement banner from the announcements repo
def get_announcement():
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

