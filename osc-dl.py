import parsecontents
import argparse
import download
import localcontents


beta_number = "5"
build = 0
version = "1.1." + beta_number

parser = argparse.ArgumentParser(
    description="Open Shop Channel Package Downloader"
)

subparser = parser.add_subparsers(dest='cmd')
subparser.add_parser('list')
query = subparser.add_parser('query')
get = subparser.add_parser('get')
getall = subparser.add_parser('get-all')
getlist = subparser.add_parser('get-list')
metadata = subparser.add_parser('meta')


if build > 0:
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version + ' (Build: ' + str(build) + ') Developed by dhtdht020. Open Source Software.')
else:
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version + ' Developed by dhtdht020. Open Source Software.')

query.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

query.add_argument(
    "-v",
    "--verify",
    help="Check if app exists and return True or False",
    action="store_true"
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
    help="Don't ask for confirmation after metadata displays.",
    action="store_true"
)

get.add_argument(
    "-o",
    "--output",
    help="Output file name",
    action="store"
)

get.add_argument(
    "-e",
    "--extract",
    help="Extract downloaded zip file to the ExtractedApps directory.",
    action="store_true"
)

getall.add_argument(
    "-o",
    "--output",
    help="Not implemented.",
    action="store"
)

getall.add_argument(
    "-e",
    "--extract",
    help="Extract downloaded zip files to the ExtractedApps directory.",
    action="store_true"
)

getlist.add_argument(
    "-f",
    "--file",
    help="List of apps to download",
    action="store",
    required=True
)

args = parser.parse_args()
if args.cmd == 'list':
    parsecontents.get()

if args.cmd == 'query':
    if args.verify is False:
        parsecontents.query(args.name)
    else:
        parsecontents.query_verify(args.name)

if args.cmd == 'meta':
    if args.type is None:
        args.type = "default"

    download.metadata(args.name, args.type)

if args.cmd == 'get-all':
    args.output = "default"
    if args.extract is None:
        args.extract = False

    download.everything(args.output, args.extract)

if args.cmd == 'get-list':
    localcontents.dl_list(args.file)

if args.cmd == 'get':
    # Skip manual approval if specified
    if args.output is None:
        args.output = "default"

    if args.extract is None:
        args.extract = False

    if args.noconfirm is True:
        if parsecontents.query(args.name) is False:
            exit(0)
        download.metadata(args.name, "default")
        download.get(args.name, args.output, args.extract)

    if args.noconfirm is False:
        if parsecontents.query(args.name) is False:
            exit(0)
        download.confirm(args.name)
        download.get(args.name, args.output, args.extract)
