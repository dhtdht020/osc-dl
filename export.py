import parsecontents
import sys


def app_list(txt_path="osc-dl_export_app_list.txt", repo="hbb1.oscwii.org"):
    if txt_path is None:
        txt_path = "osc-dl_export_app_list.txt"
    sys.stdout = open(str(txt_path), "w")
    parsecontents.get(raw=True, repo=repo)
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    print("Exported application list to " + txt_path)

