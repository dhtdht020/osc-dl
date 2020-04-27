import requests
import lxml.etree
import parsecontents
import zipfile


def get(app_name, output="default", extract=False, repo="hbb1.oscwii.org"):

    if output == "default":
        output = app_name + ".zip"

    # https://hbb1.oscwii.org/hbb/fceugx/fceugx.zip
    print("Obtaining " + app_name + " from " + repo + "..")
    u = requests.get("https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")

    with open(output, "wb") as f:
        f.write(u.content)

    print("Download success! Output: " + output)

    if extract is True:
        with zipfile.ZipFile(output, 'r') as zip_ref:
            print("Extracting..")
            zip_ref.extractall("ExtractedApps")
            print("Extracted to ExtractedApps!")


def confirm(app_name, repo="hbb1.oscwii.org"):
    # https://hbb1.oscwii.org/unzipped_apps/wiixplorer/apps/wiixplorer/
    xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    root = lxml.etree.fromstring(xml)
    display_name = root.find('name').text

    metadata(app_name, "default")

    answer = input('Continue with download of "' + display_name + '"? (y/n) > ')
    if answer == "y":
        pass
    elif answer == "n":
        print("Cancelled download operation. Exiting.")
        exit(1)
    else:
        print("Please reply with 'y' to continue or 'n' to cancel.")


def metadata(app_name, type, repo="hbb1.oscwii.org"):
    # https://hbb1.oscwii.org/unzipped_apps/wiixplorer/apps/wiixplorer/
    xml = requests.get("https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml").text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    try:
        root = lxml.etree.fromstring(xml)
    except lxml.etree.XMLSyntaxError:
        print("[Error D001] The meta.xml file for " + app_name + " seems to be broken. Oh no. Preparing for the worst..")

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


def everything(output, extract=False, repo="hbb1.oscwii.org"):
    data = parsecontents.get_list()
    progress = 0
    amount = len(data.keys())

    for key in data.keys():
        metadata(key, "default")
        get(key, "default", extract)  # remember to implement output or it's gonna be very sad
        progress = progress+1
        print("[Progress] Downloaded " + str(progress) + " out of " + str(amount) + " apps.")
