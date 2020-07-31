from zipfile import ZipFile
import requests
import lxml.etree
import parsecontents
import sys
from halo import Halo
import metadata

GREEN = '\033[92m'
FAIL = '\033[91m'


# download app, print result.
def get(app_name, output=None, extract=False, repo="hbb1.oscwii.org"):

    if output is None:
        output = app_name + ".zip"

    # https://hbb1.oscwii.org/hbb/fceugx/fceugx.zip
    # print("Obtaining " + app_name + " from " + repo + "..")
    with Halo(
            text="Obtaining " + app_name + " from " + repo + "..", color="yellow", text_color="yellow"
    ):
        try:
            app_data = requests.get("https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")
        except requests.exceptions.SSLError:
            app_data = requests.get("http://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")

    with open(output, "wb") as app_data_file:
        app_data_file.write(app_data.content)

    print(GREEN + "Download success! Output: " + output)

    if extract is True:
        with ZipFile(output, 'r') as zip_ref:
            print("Extracting..")
            zip_ref.extractall("ExtractedApps")
            print("Extracted to ExtractedApps!")


# confirmation prompt
def confirm(app_name, repo="hbb1.oscwii.org"):
    # https://hbb1.oscwii.org/unzipped_apps/wiixplorer/apps/wiixplorer/
    with Halo(text="Loading Metadata..", color="white"):
        try:
            xml = requests.get(
                "https://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml"
            ).text
        except requests.exceptions.SSLError:
            xml = requests.get(
                "http://" + repo + "/unzipped_apps/" + app_name + "/apps/" + app_name + "/meta.xml"
            ).text

    # remove unicode declaration
    xml = xml.split("\n", 1)[1]

    # get information from XML
    root = lxml.etree.fromstring(xml)
    try:
        display_name = root.find('name').text
    except AttributeError:
        print("[Error D:002] Could not find application on the server. Cannot continue.")
        sys.exit(1)

    metadata.get(app_name)

    answer = input('Continue with download of "' + display_name + '"? (y/n) > ')
    if answer == "y":
        pass
    elif answer == "n":
        print(FAIL+"Cancelled download operation. Exiting.")
        sys.exit(1)
    else:
        print("Please reply with 'y' to continue or 'n' to cancel.")


def everything(extract=False, repo="hbb1.oscwii.org"):
    data = parsecontents.get_list(repo=repo)
    progress = 0
    amount = len(data.keys())

    for key in data.keys():
        metadata.get(app_name=key, type="default", repo=repo)
        get(app_name=key, extract=extract, repo=repo)  # remember to implement output or it's gonna be very sad
        progress = progress+1
        print("[Progress] Downloaded " + str(progress) + " out of " + str(amount) + " apps.")
