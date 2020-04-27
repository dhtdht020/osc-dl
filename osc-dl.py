import parsecontents
import argparse
import download
import os


version = "1.1.0"
build = "0"

parser = argparse.ArgumentParser(
    description="Open Shop Channel Package Downloader"
)

subparser = parser.add_subparsers(dest='cmd')
subparser.add_parser('list')
query = subparser.add_parser('query')
get = subparser.add_parser('get')
getall = subparser.add_parser('get-all')
metadata = subparser.add_parser('meta')


parser.add_argument('--version', action='version', version='%(prog)s ' + version + ' Developed by dhtdht020. Open Source Software.')

query.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

get.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

metadata.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

metadata.add_argument(
    "-t",
    "--type",
    help="Type of metadata to obtain "
         "(display_name, developer, version, short_description, long_description, release_date, contributors)",
    action="store"
)

get.add_argument(
    "-c",
    "--noconfirm",
    action="store_true"
)

get.add_argument(
    "-o",
    "--output",
    action="store"
)

get.add_argument(
    "-e",
    "--extract",
    action="store_true"
)

getall.add_argument(
    "-o",
    "--output",
    action="store"
)

getall.add_argument(
    "-e",
    "--extract",
    action="store_true"
)


args = parser.parse_args()
if args.cmd == 'list':
    parsecontents.get()

if args.cmd == 'query':
    parsecontents.query(args.name)

if args.cmd == 'meta':
    if args.type is None:
        args.type = "default"

    download.metadata(args.name, args.type)

if args.cmd == 'get-all':
    args.output = "default"
    if args.extract is None:
        args.extract = False

    download.everything(args.output, args.extract)

if args.cmd == 'get':
    # Skip manual approval if specified
    if args.output is None:
        args.output = "default"

    if args.extract is None:
        args.extract = False

    if args.noconfirm is True:
        if parsecontents.query(args.name) is False:
            os.remove("metadata.json")
            exit(0)
        download.metadata(args.name, "default")
        download.get(args.name, args.output, args.extract)

    if args.noconfirm is False:
        if parsecontents.query(args.name) is False:
            os.remove("metadata.json")
            exit(0)
        download.confirm(args.name)
        download.get(args.name, args.output, args.extract)
