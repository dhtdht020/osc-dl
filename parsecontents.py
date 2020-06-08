import requests
import json
from halo import Halo

FAIL = '\033[91m'


# Get list of apps from repo metadata
def get(repo="hbb1.oscwii.org", raw=False):
    if raw is False:
        with Halo(text="Getting list..", color="yellow", text_color="yellow"):
            u = requests.get("https://" + repo + "/metadata.json")
    else:
        u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)
    for key in data.keys():
        print(key)


def query(term, repo="hbb1.oscwii.org"):
    print("Searching for package on " + repo + "..")
    with Halo(text="Searching..", color="yellow", text_color="yellow"):
        u = requests.get("https://" + repo + "/metadata.json")

    try:
        data = json.loads(u.content)
    except json.decoder.JSONDecodeError:
        print("[Error P:001] Could not parse list from metadata JSON.")
        exit(1)

    found = "false"

    for key in data.keys():
        if key == term:
            found = "true"

    if found == "true":
        print("Found package!")
        return True
    else:
        print(FAIL+'Could not find "' + term + '" on the repository. :(')


def query_verify(term, repo="hbb1.oscwii.org", internal=False):
    u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)

    found = "false"

    for key in data.keys():
        if key == term:
            found = "true"

    if internal is False:
        if found == "true":
            return print("True")
        else:
            return print("False")
    else:
        if found == "true":
            return True
        else:
            return False


def get_list(repo="hbb1.oscwii.org"):
    print("Getting list of all packages from " + repo + "..")

    with Halo(text="Getting list..", color="yellow", text_color="yellow"):
            u = requests.get("https://" + repo + "/metadata.json")

    try:
        data = json.loads(u.content)
    except json.decoder.JSONDecodeError:
        print("[Error P:001:2] Could not parse list from metadata JSON.")
        exit(1)

    return data


def list(repo="hbb1.oscwii.org"):
    try:
        u = requests.get("https://" + repo + "/metadata.json")
    except requests.exceptions.SSLError:
        u = requests.get("http://" + repo + "/metadata.json")

    applist = []

    data = json.loads(u.content)
    for key in data.keys():
        applist.append(key)

    return applist


def repository_list(repo="hbb1.oscwii.org"):
    print("Getting raw list of all repositories from " + repo + "..\n\n")
    with Halo(text="Loading Secondary Repositories..", color="yellow", text_color="yellow"):
        u = requests.get("https://" + repo + "/hbb/repo_list.txt").text

    print(u)
