import parsecontents
import argparse
import download
import localcontents


beta_number = "4"
build = 0
version = "1.2." + beta_number

parser = argparse.ArgumentParser(
    description="Open Shop Channel Package Downloader"
)

subparser = parser.add_subparsers(dest='cmd')
applist = subparser.add_parser('list')
query = subparser.add_parser('query')
get = subparser.add_parser('get')
getall = subparser.add_parser('get-all')
getlist = subparser.add_parser('get-list')
metadata = subparser.add_parser('meta')
repolist = subparser.add_parser('repo-list')


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

query.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
)

get.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

get.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
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

metadata.add_argument(
    "-r",
    "--host",
    help="Repository URL",
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

getall.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
)

getlist.add_argument(
    "-f",
    "--file",
    help="List of apps to download",
    action="store",
    required=True
)

getlist.add_argument(
    "-d",
    "--display",
    help="Prints list and doesn't download",
    action="store_true"
)

getlist.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
)

applist.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
)

args = parser.parse_args()


# list of apps on server command
if args.cmd == 'list':
    if args.host is None:
        args.host = "hbb1.oscwii.org"
    parsecontents.get(repo=args.host)


# query app command
if args.cmd == 'query':
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.verify is False:
        parsecontents.query(args.name, repo=args.host)
    else:
        parsecontents.query_verify(args.name, repo=args.host)


# get metadata command
if args.cmd == 'meta':
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.type is None:
        args.type = "default"

    download.metadata(app_name=args.name, type=args.type, repo=args.host)


# get list of repos on server command
if args.cmd == 'repo-list':
    parsecontents.repository_list()


# get the entire repo command
if args.cmd == 'get-all':
    args.output = "default"

    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.extract is None:
        args.extract = False

    download.everything(output=args.output, extract=args.extract, repo=args.host)


# get list file command
if args.cmd == 'get-list':
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.display is True:
        localcontents.dl_list(file=args.file, display=True, repo=args.host)
    else:
        localcontents.dl_list(file=args.file, repo=args.host)


# get command
if args.cmd == 'get':
    # Skip manual approval if specified
    if args.output is None:
        args.output = "default"

    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.extract is None:
        args.extract = False

    if args.noconfirm is True:
        if parsecontents.query(args.name, repo=args.host) is False:
            exit(0)
        download.metadata(args.name, "default", repo=args.host)
        download.get(args.name, args.output, args.extract, repo=args.host)

    if args.noconfirm is False:
        if parsecontents.query(args.name, repo=args.host) is False:
            exit(0)
        download.confirm(args.name, repo=args.host)
        download.get(args.name, args.output, repo=args.host)
