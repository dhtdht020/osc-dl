import parsecontents
import argparse
import download
import localcontents
import updater
import metadata
import export
import os

if os.name == 'nt':
    # Initialize color on Windows
    os.system('color')

build = 0
year = "2020"

osc_dl = os.path.basename(__file__)

parser = argparse.ArgumentParser(
    description="Open Shop Channel Package Downloader"
)

subparser = parser.add_subparsers(dest='cmd')
applist = subparser.add_parser('list')
query = subparser.add_parser('query')
get = subparser.add_parser('get')
getall = subparser.add_parser('get-all')
getlist = subparser.add_parser('get-list')
meta = subparser.add_parser('meta')
repolist = subparser.add_parser('repo-list')
export_cmd = subparser.add_parser('export')
update = subparser.add_parser('update')


if build > 0:
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + updater.current_version() + ' (Build: ' + str(build) + ') Developed by dhtdht020. Open Source Software.')
else:
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + updater.current_version() + ' Developed by dhtdht020. Open Source Software.')

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

meta.add_argument(
    "-n",
    "--name",
    help="Name of homebrew app",
    required=True
)

meta.add_argument(
    "-t",
    "--type",
    help="Type of metadata to obtain "
         "(display_name, developer, version, short_description, long_description, release_date, contributors)",
    action="store"
)

meta.add_argument(
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

applist.add_argument(
    "--raw",
    help="No spinner.",
    action="store_true"
)

export_cmd.add_argument(
    "-o",
    "--output",
    help="Output file",
    action="store"
)

export_cmd.add_argument(
    "-t",
    "--type",
    help="Type of data to export "
         "(list)",
    action="store",
    required=True
)

export_cmd.add_argument(
    "-r",
    "--host",
    help="Repository URL",
    action="store"
)

ascii_logo = """                                                                                                    
    `.----.   .--`----.     `....`   ---.-:::.    
   :++/-:/++- :///---///` `---...--` +oo+:::oo+`  
  :++-    :++.://`   `///`--.```.---`+oo    :oo.  
  :++`    -++-://`    ///`----....`` +oo    :oo.  
  .++/.``./+/`://:```://- ---`` ``-. +oo    :oo.  
   `-//++/:-  ://::///:.   `.-----.` ///    -//.  
              ://`                                
              ---       Downloader Version """ + updater.current_version() + """                                                                   
"""

args = parser.parse_args()

# if no argument
if args.cmd is None:
    print(ascii_logo)
    print("Open Source Software, "+year+". Developed by dhtdht020 @ GitHub.")
    print("\nRun \""+osc_dl+" --help\" for help.")


# list of apps on server command
if args.cmd == 'list':
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    parsecontents.get(repo=args.host, raw=args.raw)


# update osc-dl command
if args.cmd == 'update':
    updater.init_update()


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

    appmeta = metadata.get(app_name=args.name, type=args.type, repo=args.host)
    if appmeta is not None:
        print(appmeta)


# get list of repos on server command
if args.cmd == 'repo-list':
    parsecontents.repository_list()


# export data to file command
if args.cmd == 'export':
    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.type == "list":
        export.app_list(repo=args.host)


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
        args.output = None

    if args.host is None:
        args.host = "hbb1.oscwii.org"

    if args.extract is None:
        args.extract = False

    if args.noconfirm is True:
        if parsecontents.query(term=args.name, repo=args.host) is False:
            exit(0)
        metadata.get(app_name=args.name, type="default", repo=args.host)
        download.get(app_name=args.name, output=args.output, extract=args.extract, repo=args.host)

    if args.noconfirm is False:
        if parsecontents.query(term=args.name, repo=args.host) is False:
            exit(0)
        download.confirm(app_name=args.name, repo=args.host)
        download.get(app_name=args.name, output=args.output, repo=args.host)
