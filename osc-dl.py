import argparse
import io
import os
import threading
import time
from datetime import datetime
from zipfile import ZipFile

import requests
import serial

import wiiload
import updater
import api
from utils import file_size

if os.name == 'nt':
    # Initialize color on Windows
    os.system('color')

repos = api.Hosts()

parser = argparse.ArgumentParser(add_help=False,
                                 description=f"Open Shop Channel Downloader v{updater.current_version()} {updater.get_branch()}",
                                 epilog="OSCDL, Open Source Software by dhtdht020. https://github.com/dhtdht020.")
subparser = parser.add_subparsers(dest='cmd')

# Set help information
parser._positionals.title = 'The following commands are available'
parser._optionals.title = 'The following options are available'
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Displays an help screen like this one.')

# Get - downloads application
get = subparser.add_parser(name='get', help="Download application.")
# Send - downloads and sends application over TCP/IP
send = subparser.add_parser(name='send', help="Send application to Wii via the network or USBGecko.")
# Show - displays information about an application
show = subparser.add_parser(name='show', help="Show information about an application.")
# Hosts - displays available repositories
hosts = subparser.add_parser(name='hosts', help="List available hosts.")

# Get arguments
get.add_argument("app", type=str,
                 help="App to download. (e.g. WiiVNC)")
get.add_argument("-r", "--host", type=str,
                 help="Repository name (e.g. primary)", default="primary")

# Send arguments
send.add_argument("app", type=str,
                  help="App to send. (e.g. WiiVNC)")
send.add_argument("-g", "--gecko", help="Use USBGecko protocol", action='store_true')
send.add_argument("-d", "--destination", type=str,
                  help="Wii IP/USBGecko address (e.g. 192.168.1.10, COM# for Windows, /dev/cu.* for UNIX)",
                  required=True)
send.add_argument("-r", "--host", type=str,
                  help="Repository name (e.g. primary)", default="primary")

# Show arguments
show.add_argument("app", type=str,
                  help="App to show. (e.g. WiiVNC)")
show.add_argument("-r", "--host", type=str,
                  help="Repository name (e.g. primary)", default="primary")

args = parser.parse_args()


# legacy function. todo: should be rewritten
def download(app_name, output=None, extract=False, repo="hbb1.oscwii.org"):
    if output is None:
        output = app_name + ".zip"

    app_data = requests.get("https://" + repo + "/hbb/" + app_name + "/" + app_name + ".zip")

    if app_data.status_code == 200:
        with open(output, "wb") as app_data_file:
            app_data_file.write(app_data.content)

        # Extract to ExtractedApps if needed
        if extract is True:
            with ZipFile(output, 'r') as zip_ref:
                zip_ref.extractall("ExtractedApps")

        print("Download success! Output: " + output)

    else:
        print(f"Download failed. HTTP status code is {str(app_data.status_code)}, not 200.")


if not args.cmd:
    parser.parse_args(["-h"])
# Get
if args.cmd == "get":
    if args.app == "all":
        applications = api.Applications(repos.get(args.host))
        print(f"Starting download of all packages from \"{args.host}\" @ {repos.get(args.host)['host']}..")
        for package in applications.get_apps():
            download(app_name=package["internal_name"], repo=repos.get(args.host)["host"])
    else:
        download(app_name=args.app, repo=repos.get(args.host)["host"])

# Send
if args.cmd == "send":
    # get hostname of host
    host_url = repos.get(args.host)["host"]

    if not args.gecko:
        ok = wiiload.validate_ip_regex(ip=args.destination)
        if not ok:
            print(f"Error: The address '{args.destination}' is invalid! Please correct it!")
            exit(1)

    url = f"https://{host_url}/hbb/{args.app}/{args.app}.zip"
    r = requests.get(url)
    zipped_app = io.BytesIO(r.content)
    zip_buf = io.BytesIO()

    # Our zip file should only contain one directory with the app data in it,
    # but the downloaded file contains an apps/ directory. We're removing that here.
    wiiload.organize_zip(zipped_app, zip_buf)

    # preparing
    print("Preparing app..")
    prep = wiiload.prepare(zip_buf)

    file_size = prep[0]
    compressed_size = prep[1]
    chunks = prep[2]
    c_data = prep[3]

    # connecting
    print('Connecting to the Homebrew Channel..')

    try:
        if args.gecko:
            conn = serial.Serial(args.destination)
            conn.send = conn.write  # This is done to keep wiiload.py the same.
        else:
            conn = wiiload.connect(args.destination)

    except Exception as e:
        if args.gecko:
            errmsg = "serial connection"
        else:
            errmsg = "IP address"

        print('Connection error: Error while connecting to the Homebrew Channel.\n'
              f'Please check the {errmsg} and try again.')

        print(f'Exception: {e}')
        print('Error: Could not connect to the Homebrew Channel. :(')
        exit(1)

    wiiload.handshake(conn, compressed_size, file_size)

    # Sending file
    if not args.gecko:
        print('[  0%] Sending app..')

        chunk_num = 1
        for chunk in chunks:
            try:
                conn.send(chunk)
            except Exception as e:
                print('Error while connecting to the HBC. Operation timed out. Close any dialogs on HBC and try again.')

                print(f'Exception: {e}')
                print('Error: Could not connect to the Homebrew Channel. :(')

                # delete application zip file
                conn.close()
                exit(1)

            chunk_num += 1
            progress = round(chunk_num / len(chunks) * 50) + 50
            if progress < 100:
                print(f'[ {progress}%] Sending app..')
            if progress == 100:
                print(f'[{progress}%] Sending app..')
    else:
        print('Sending app..', end="")
        t = threading.Thread(target=wiiload.send_gecko, daemon=True, args=[c_data, conn])
        t.start()
        while t.is_alive():
            print(".", end="")
            time.sleep(0.5)
        t.join()
        if not wiiload.DATASENT:
            exit(1)
        print()

    file_name = f'{args.app}.zip'
    conn.send(bytes(file_name, 'utf-8') + b'\x00')
    if args.gecko:
        conn.flush()
        conn.close()

    print(f'App sent to Wii at {args.destination} successfully!')

# Hosts
if args.cmd == "show":
    applications = api.Applications(repos.get(args.host))
    app = applications.get_by_name(args.app)
    if app:
        print("Found \"{}\" [{}]".format(app["display_name"], app["internal_name"]))
        print("Category: {}".format(app["category"]))
        print("Version: {}".format(app["version"]))
        print("Description: {}".format(app["long_description"]))
        print("Short Description: {}".format(app["short_description"]))
        print("Release Date: {}".format(datetime.fromtimestamp
                                        (int(app["release_date"])).strftime('%B %e, %Y at %R')))
        print("Publisher: {}".format(app["coder"]))
        print("Package:")
        print("  Type: {}".format(app["package_type"]))
        print("  Download Size: {}".format(file_size(app["zip_size"])))
        print("  Extracted Size: {}".format(file_size(app["extracted"])))

# Hosts
if args.cmd == "hosts":
    print(f"Total of {len(repos.list())} hosts found:")
    n = 1
    for host in repos.list():
        name = host
        host = repos.list()[host]
        print("\n{}. {} ({}):".format(n, host["name"], name))
        print("   Description: {}".format(host["description"]))
        print("   Example Usage: \"oscdl get WiiVNC -r {}\"".format(name))
        n += 1
