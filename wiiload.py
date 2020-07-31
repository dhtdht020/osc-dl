import re
import zipfile
import copy

IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


def validate_ip_regex(ip):
    # check IP address against regex
    ip_match = IP_REGEX.match(ip)
    return ip_match


def organize_zip(zipped_app, zip_buf):
    zip_file = zipfile.ZipFile(zipped_app, mode='r')
    app_infolist = zip_file.infolist()

    # Our zip file should only contain one directory with the app data in it,
    # but the downloaded file contains an apps/ directory. We're removing that here.
    app_zip = zipfile.ZipFile(zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED)

    # copy over all files
    for info in app_infolist:
        new_path = info.filename.replace('apps/', '')
        if not new_path:
            continue

        # we need to copy over the member info manually because
        # python's zipfile implementation sucks and
        # the HBC is very insecure about it.
        new_info = copy.copy(info)
        new_info.filename = new_path

        if new_info.filename[-1] in ('/', '\\'):  # directory
            continue

        with zip_file.open(info.filename, 'r') as file:
            data = file.read()

        app_zip.writestr(new_path, data)

    # cleanup
    zipped_app.close()
    zip_file.close()
    app_zip.close()
