import requests
import json


# Get list of apps from repo metadata
def get(repo="hbb1.oscwii.org"):
    u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)
    for key in data.keys():
        print(key)


def query(term, repo="hbb1.oscwii.org"):
    print("Searching for package on " + repo + "..")
    u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)

    found = "false"

    for key in data.keys():
        if key == term:
            found = "true"

    if found == "true":
        print("Found package!")
        return True
    else:
        print('Could not find "' + term + '" on the repository. :(')


def query_verify(term, repo="hbb1.oscwii.org"):
    u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)

    found = "false"

    for key in data.keys():
        if key == term:
            found = "true"

    if found == "true":
        return print("True")
    else:
        return print("False")


def get_list(repo="hbb1.oscwii.org"):
    print("Getting list of all packages from " + repo + "..")
    u = requests.get("https://" + repo + "/metadata.json")

    data = json.loads(u.content)

    return data


def repository_list(repo="hbb1.oscwii.org"):
    print("Getting raw list of all repositories from " + repo + "..\n\n")
    u = requests.get("https://" + repo + "/hbb/repo_list.txt").text

    print(u)
