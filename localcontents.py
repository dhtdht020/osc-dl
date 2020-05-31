import download
import parsecontents
import metadata


def dl_list(file, display="False", repo="hbb1.oscwii.org"):
    for line in open(file):  # if anyone has any idea how to make this less hacky then please help
        try:
            line = line.rstrip("\n\r")
        except Exception:
            pass

        try:
            line = line.rstrip("\n")
        except Exception:
            pass

        if line is "":
            pass
        else:
            if display is True:
                print(line)
            else:
                if parsecontents.query(term=line, repo=repo) is True:
                    metadata.get(app_name=line, type="default", repo=repo)
                    download.get(app_name=line, repo=repo)
