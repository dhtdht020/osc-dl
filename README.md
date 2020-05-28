# Open Shop Channel DL [![Actions Status](https://github.com/dhtdht020/osc-dl/workflows/Build/badge.svg)](https://github.com/dhtdht020/osc-dl/actions) [![Discord Server](https://img.shields.io/discord/426478571389976577.svg)](https://discord.gg/by6mR5N) [![Downloads](https://img.shields.io/github/downloads/dhtdht020/osc-dl/total)](https://github.com/dhtdht020/osc-dl/releases) [![License](https://img.shields.io/badge/Open%20Source-GPL--3.0-lightgrey.svg)](https://github.com/dhtdht020/osc-dl/blob/master/LICENSE)

OSC-DL is an advanced Python 3 command line utility for obtaining homebrew from the Open Shop Channel repository, and scraping it's contents.

Soon, it will be available as a PIP package for use in other projects that require obtaining homebrew applications.

Currently, the following features are implemented:

- Listing all apps on the remote repository.
- Obtaining and parsing metadata.
- Downloading individual apps or the entire repository.

![Preview](https://cdn.discordapp.com/attachments/539096161831616523/704315841696497804/cmd_qOe9l3mnc9.png "Preview")

## Installing OSC-DL

I recommend using the latest [release build](https://github.com/dhtdht020/osc-dl/releases), as it's a onefile variation of the program useful for avoiding dependency hell.

##### Manual Download:

Make sure Python 3 is installed and used.

1. `git clone https://github.com/dhtdht020/osc-dl.git`
2. `cd osc-dl`
2. `pip3 install -r requirements.txt`
3. `python3 osc-dl.py`


## Downloading Homebrew (get command)

You can download homebrew from the Open Shop Channel by using `osc-dl get`

Example usage: `osc-dl get -n wiixplorer`

The following arguments can be used

- `-n / --name` Required. Name of homebrew app to download
- `-c / --noconfirm` Disable download confirmation message after application metadata displays.
- `-o / --output` Output file name.

## Homebrew Metadata (meta command)

You can obtain visual metadata or metadata items about homebrew applications in the Open Shop Channel by using `osc-dl meta`

Example usage: `osc-dl meta -n wiixplorer`

Example output: 
```
=========== Application Metadata ===========
Application: WiiXplorer

Developer: Dimok
Version: r259
Description: Wii File Browser
============================================
```

Example usage: `osc-dl meta -n wiixplorer -t version`

Example output:
```
r259
```


The following arguments can be used

- `-n / --name` Required. Name of homebrew app to obtain metadata for.
- `-t / --type` Type of metadata to obtain (display_name, developer, version, short_description, long_description, release_date, contributors)
- `-o / --output` Output file name.

## List Homebrew (list command)

You can list the names of all homebrew on the Open Shop Channel repository by using `osc-dl list`

Example usage: `osc-dl list`

Currently, there are no arguments, although a way to filter the results or save to a file is planned.

## Querying Homebrew (query command)

You can search homebrew available on the Open Shop Channel by using `osc-dl query`

Example usage: `osc-dl query -n wiixplorer`

This command is unfinished, and can currently only check for exact matches.

The following arguments can be used

- `-n / --name` Required. Name of homebrew app to query.
- `-v / --verify` Caused query to return "True" if the app is present and "False" if it isn't.

## Download Everything (get-all command)

This command was intended for debugging, and we don't recommend using it, as it might have an unexpected behaviour.

Example usage: `osc-dl get-all`

This command is not maintained nor supported, and although specified in help, setting output directory is not possible at the time.



