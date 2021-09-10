from zipfile import ZipFile
import requests

GREEN = '\033[92m'
FAIL = '\033[91m'


# download app from the open shop channel
def get(app_name, output=None, extract=False, repo="hbb1.oscwii.org"):
    if output is None:
        output = app_name + ".zip"

    try:
        app_data = requests.get("https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")
    except requests.exceptions.SSLError:
        app_data = requests.get("http://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")

    if app_data.status_code == 200:
        with open(output, "wb") as app_data_file:
            app_data_file.write(app_data.content)

        # Extract to ExtractedApps if needed
        if extract is True:
            with ZipFile(output, 'r') as zip_ref:
                zip_ref.extractall("ExtractedApps")

        print(GREEN + "Download success! Output: " + output)

    else:
        print(FAIL + f"Download failed. HTTP status code is {str(app_data.status_code)}, not 200.")


def get_url(app_name, repo="hbb1.oscwii.org"):
    return "https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip"
