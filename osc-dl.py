import argparse
import io
import requests

import download
import wiiload

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='cmd')

get = subparser.add_parser('get')
send = subparser.add_parser('send')

# Get arguments
get.add_argument("app", type=str,
                 help="App to download. (e.g. WiiVNC)")
get.add_argument("-r", "--host", type=str,
                 help="Repository address (e.g. hbb1.oscwii.org)")

# Send arguments
send.add_argument("app", type=str,
                  help="App to send. (e.g. WiiVNC)")
send.add_argument("-d", "--destination", type=str,
                  help="Wii IP address (e.g. 192.168.1.10)", required=True)
send.add_argument("-r", "--host", type=str,
                  help="Repository address (e.g. hbb1.oscwii.org)")

args = parser.parse_args()

# Get
if args.cmd == "get":
    if args.host:
        download.get(app_name=args.app, repo=args.host)
    else:
        download.get(app_name=args.app)

# Send
if args.cmd == "send":
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    ok = wiiload.validate_ip_regex(ip=args.destination)
    if not ok:
        print(f"The IP address '{args.destination}' is invalid! Please correct it!")
        exit(1)

    url = f"https://{args.host}/hbb/{args.app}/{args.app}.zip"
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
