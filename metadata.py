import parsecontents
import requests
import lxml.etree

GREEN = '\033[92m'
FAIL = '\033[91m'


def get(app_name, type=None, repo="hbb1.oscwii.org"):
    if parsecontents.query_verify(term=app_name, repo=repo, internal=True) is False:
        print(FAIL+"Failure: App "+app_name+" could not be found on "+repo)
        exit(1)

    # https://hbb1.oscwii.org/unzipped_apps/wiixplorer/apps/wiixplorer/
    xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

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

    try:
        long_description = root.find('long_description').text
    except Exception:
        long_description = "Unknown"

    try:
        release_date = root.find('release_date').text
    except Exception:
        release_date = "Unknown"

    try:
        contributors = root.find('contributors').text
    except Exception:
        contributors = "Unknown"

    # check for requested information
    if type == "display_name":
        return print(display_name)

    if type == "coder":
        return print(developer)

    if type == "version":
        return print(version)

    if type == "short_description":
        return print(short_description)

    if type == "long_description":
        return print(long_description)

    if type == "release_date":
        return print(release_date)

    if type == "contributors":
        return print(contributors)

    print("\n=========== Application Metadata ===========")
    print("Application: " + display_name + "\n")
    print("Developer: " + developer)
    print("Version: " + version)
    print("Description: " + short_description)
    print("============================================\n")
