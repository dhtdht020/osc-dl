import parsecontents
import requests
import lxml.etree
import dateparser
import locale


GREEN = '\033[92m'
FAIL = '\033[91m'
try:
    locale.setlocale(locale.LC_ALL, 'en_GB')
except locale.Error:
    pass



def get(app_name, type=None, repo="hbb1.oscwii.org"):
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
        return display_name

    if type == "coder":
        return developer

    if type == "version":
        return version

    if type == "short_description":
        return short_description

    if type == "long_description":
        return long_description

    if type == "release_date":
        return release_date

    if type == "contributors":
        return contributors

    print("\n=========== Application Metadata ===========")
    print("Application: " + display_name + "\n")
    print("Developer: " + developer)
    print("Version: " + version)
    print("Description: " + short_description)
    print("============================================\n")


# experimental, for use by xosc-dl
def icon(app_name, repo="hbb1.oscwii.org"):
    try:
        request = requests.get("https://" + repo+ "/hbb/"+ app_name + ".png")
        icon = request.content
        # If icon is not there
        if str(request.status_code) != "200":
            icon = requests.get(
                "https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/assets/missing.png").content
    except Exception:
        icon = requests.get("https://raw.githubusercontent.com/dhtdht020/oscdl-updateserver/master/v1/assets/missing.png").content
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
        try:
            parsed_date = dateparser.parse(root.find('release_date').text)
            if parsed_date is not None:
                readable_date = parsed_date.strftime('%x')
                release_date = root.find('release_date').text + " (" + readable_date + ")"
            else:
                release_date = root.find('release_date').text + " [RAW]"
        except Exception:
            release_date = root.find('release_date').text + " [RAW]"
    except Exception:
        release_date = "Unknown"

    try:
        contributors = root.find('contributors').text
    except Exception:
        contributors = "None"

    meta = {"display_name": display_name,
            "coder": developer,
            "version": version,
            "short_description": short_description,
            "long_description": long_description,
            "release_date": release_date,
            "contributors": contributors
            }

    return meta


def file_size(app_name, repo="hbb1.oscwii.org"):
    try:
        response = requests.get(f"https://{repo}/hbb/{app_name}/{app_name}.zip", stream=True)
    except requests.exceptions.SSLError:
        response = requests.get(f"http://{repo}/hbb/{app_name}/{app_name}.zip", stream=True)

    length = int(response.headers['Content-length'])
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
