import argparse
import io
from datetime import datetime

import requests

import download
import metadata
import wiiload
import hosts as repos

repos = repos.Hosts()

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='cmd')

# Get - downloads application
get = subparser.add_parser(name='get', help="Download application.")
# Send - downloads and sends application
send = subparser.add_parser(name='send', help="Send application to Wii.")
# Show - displays information about an application
show = subparser.add_parser(name='show', help="Show information about an application.")
# Hosts - displays available repositories
hosts = subparser.add_parser(name='hosts', help="List of available hosts.")

# Get arguments
get.add_argument("app", type=str,
                 help="App to download. (e.g. WiiVNC)")
get.add_argument("-r", "--host", type=str,
                 help="Repository name (e.g. primary)", default="primary")

# Send arguments
send.add_argument("app", type=str,
                  help="App to send. (e.g. WiiVNC)")
send.add_argument("-d", "--destination", type=str,
                  help="Wii IP address (e.g. 192.168.1.10)", required=True)
send.add_argument("-r", "--host", type=str,
                  help="Repository name (e.g. primary)", default="primary")

# Show arguments
show.add_argument("app", type=str,
                  help="App to show. (e.g. WiiVNC)")
show.add_argument("-r", "--host", type=str,
                  help="Repository name (e.g. primary)", default="primary")

args = parser.parse_args()

# Get
if args.cmd == "get":
    download.get(app_name=args.app, repo=repos.name(args.host)["host"])

# Send
if args.cmd == "send":
    # get hostname of host
    host_url = repos.name(args.host)["host"]

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

    # connecting
    print('Connecting to the Homebrew Channel..')

    try:
        conn = wiiload.connect(args.destination)
    except Exception as e:
        print('Connection error: Error while connecting to the Homebrew Channel.\n'
              'Please check the IP address and try again.')

        print(f'Exception: {e}')
        print('Error: Could not connect to the Homebrew Channel. :(')
        exit(1)

    wiiload.handshake(conn, compressed_size, file_size)

    # Sending file
    print('[  0%] Sending app..')

    chunk_num = 1
    for chunk in chunks:
        conn.send(chunk)

        chunk_num += 1
        progress = round(chunk_num / len(chunks) * 50) + 50
        if progress < 100:
            print(f'[ {progress}%] Sending app..')
        if progress == 100:
            print(f'[{progress}%] Sending app..')

    file_name = f'{args.app}.zip'
    conn.send(bytes(file_name, 'utf-8') + b'\x00')

    print(f'App sent to Wii at {args.destination} successfully!')

# Hosts
if args.cmd == "show":
    metadata_api = metadata.API()
    metadata_api.set_host(args.host)
    information = metadata_api.information(args.app)
    if information:
        print("Found \"{}\" [{}]".format(information["display_name"], information["internal_name"]))
        print("Category: {}".format(information["category"]))
        print("Version: {}".format(information["version"]))
        print("Description: {}".format(information["long_description"]))
        print("Short Description: {}".format(information["short_description"]))
        print("Release Date: {}".format(datetime.fromtimestamp
                                        (int(information["release_date"])).strftime('%B %e, %Y at %R')))
        print("Publisher: {}".format(information["coder"]))
        print("Package:")
        print("  Type: {}".format(information["package_type"]))
        print("  Download Size: {}".format(metadata.file_size(information["zip_size"])))
        print("  Extracted Size: {}".format(metadata.file_size(information["extracted"])))


# Hosts
if args.cmd == "hosts":
    print(f"Total of {len(repos.list())} hosts found:")
    n = 1
    for host in repos.list():
        print("\n{}. {} ({}):".format(n, host["display_name"], host["name"]))
        print("   Description: {}".format(host["description"]))
        print("   Example Usage: \"oscdl get WiiVNC -r {}\"".format(host["name"]))
        n += 1
