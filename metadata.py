import os
import sys

import parsecontents
import requests
import lxml.etree
import locale


GREEN = '\033[92m'
FAIL = '\033[91m'
try:
    locale.setlocale(locale.LC_ALL, 'en_GB')
except locale.Error:
    pass


# Get resource when frozen with PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get(app_name, repo="hbb1.oscwii.org"):
    if parsecontents.query_verify(term=app_name, repo=repo, internal=True) is False:
        print(FAIL+"Failure: App "+app_name+" could not be found on "+repo)
        exit(1)

    # https://hbb1.oscwii.org/unzipped_apps/wiixplorer/apps/wiixplorer/
    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    try:
        root = lxml.etree.fromstring(xml)
    except lxml.etree.XMLSyntaxError:
        print("[Error D:001] The meta.xml file for " + app_name + " seems to be broken. Oh no. Preparing for the worst..")

    try:
        display_name = root.find('name').text
    except Exception:
        display_name = app_name

    try:
        developer = root.find('coder').text
    except Exception:
        developer = "Unknown"

    try:
        version = root.find('version').text
    except Exception:
        version = "Unknown"

    try:
        short_description = root.find('short_description').text
    except Exception:
        short_description = "Unknown"

    print("\n=========== Application Metadata ===========")
    print(f"Application:  {display_name}")
    print(f"Developer:    {developer}")
    print(f"Version:      {version}")
    print(f"Description:  {short_description}")
    print("============================================\n")


def icon(app_name, repo="hbb1.oscwii.org"):
    try:
        request = requests.get("https://" + repo+ "/hbb/"+ app_name + ".png")
        icon = request.content
        # If icon is not there
        if str(request.status_code) != "200":
            with open(resource_path("assets/gui/missing.png"), mode='rb') as file:
                icon = file.read()
                file.close()
            # icon = resource_path("assets/gui/missing.png")
    except Exception:
        with open(resource_path("assets/gui/missing.png"), mode='rb') as file:
            icon = file.read()
            file.close()
    return icon


def url(app_name, repo="hbb1.oscwii.org"):
    app_url = "https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip"
    return app_url


def dictionary(app_name, repo="hbb1.oscwii.org"):

    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    try:
        root = lxml.etree.fromstring(xml)
    except Exception:
        pass

    try:
        display_name = root.find('name').text
    except Exception:
        display_name = app_name + " (hbbID)"

    try:
        developer = root.find('coder').text
    except Exception:
        developer = "Unknown"

    try:
        version = root.find('version').text
    except Exception:
        version = "Unknown"

    try:
        short_description = root.find('short_description').text
    except Exception:
        short_description = "No description provided"

    try:
        long_description = root.find('long_description').text
    except Exception:
        long_description = "No description provided"

    try:
        contributors = root.find('contributors').text
    except Exception:
        contributors = "None"

    meta = {"display_name": display_name,
            "coder": developer,
            "version": version,
            "short_description": short_description,
            "long_description": long_description,
            "contributors": contributors
            }

    return meta


def file_size(length):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(length) < 1024.0:
            return "%3.1f%s%s" % (length, unit, "B")
        length /= 1024.0

    return "%.1f%s%s" % (length, 'Yi', "B")


def dictionary_raw(app_name, repo="hbb1.oscwii.org"):

    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    try:
        root = lxml.etree.fromstring(xml)
    except Exception:
        pass

    d = {}
    for Element in root:
        d[Element.tag] = root.find(Element.tag).text

    return d


def raw(app_name, repo="hbb1.oscwii.org"):
    try:
        xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text
    except requests.exceptions.SSLError:
        xml = requests.get("http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    return xml
