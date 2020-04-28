import download
import parsecontents


def dl_list(file):
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
            if parsecontents.query(line) is True:
                download.metadata(line, "default")
                download.get(line)
