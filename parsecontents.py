import requests
import os
import json


# Get list of apps from repo metadata
def get(repo="hbb1.oscwii.org"):
    u = requests.get("https://" + repo + "/metadata.json")

    with open("metadata.json", "wb") as f:  # I want to change this, as this writes to disk
        f.write(u.content)

    with open('metadata.json') as f:
        data = json.load(f)
        for key in data.keys():
            print(key)

    os.remove("metadata.json")


def query(term, repo="hbb1.oscwii.org"):
    print("Searching for package on " + repo + "..")
    u = requests.get("https://" + repo + "/metadata.json")

    with open("metadata.json", "wb") as f:  # I want to change this, as this writes to disk
        f.write(u.content)

    with open('metadata.json') as f:
        data = json.load(f)

        found = "false"

        for key in data.keys():
            if key == term:
                found = "true"

        if found == "true":
            print("Found package!")
        else:
            print('Could not find "' + term + '" on the repository. :(')
            return False

    try:
        os.remove("metadata.json")
    except Exception:
        print("[Error P001] Cannot delete metadata.json. Please delete it yourself. D:")


def get_list(repo="hbb1.oscwii.org"):
    print("Getting list of all packages from " + repo + "..")
    u = requests.get("https://" + repo + "/metadata.json")

    with open("metadata.json", "wb") as f:  # I want to change this, as this writes to disk
        f.write(u.content)

    with open('metadata.json') as f:
        data = json.load(f)

    os.remove("metadata.json")
    return data
