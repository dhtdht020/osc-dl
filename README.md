
# Open Shop Channel DL [![Actions Status](https://github.com/dhtdht020/osc-dl/workflows/Build/badge.svg)](https://github.com/dhtdht020/osc-dl/actions) [![Discord Server](https://img.shields.io/discord/426478571389976577.svg)](https://discord.gg/by6mR5N) [![Downloads](https://img.shields.io/github/downloads/dhtdht020/osc-dl/total)](https://github.com/dhtdht020/osc-dl/releases) [![License](https://img.shields.io/badge/Open%20Source-GPL--3.0-lightgrey.svg)](https://github.com/dhtdht020/osc-dl/blob/master/LICENSE)

OSCDL is a cross platform desktop client for the Open Shop Channel homebrew repository, in Python 3 and Qt.

With OSCDL, you can download hundreds of homebrew apps and themes to your computer or wirelessly send them directly to the Wii.

OSCDL also supports USBGecko connections if the Wii cannot connect via LAN.

![Preview](https://user-images.githubusercontent.com/18469146/144217304-b690eba3-4c71-4791-9705-6dd36c0a1fcd.png)

## Installing OSCDL

I recommend obtaining the latest release from [here](https://github.com/dhtdht020/osc-dl/releases) if you are a Windows user.
##### Manual Download:

Make sure Python 3 is installed and used.

1. `git clone https://github.com/dhtdht020/osc-dl.git`
2. `cd osc-dl`
2. `pip3 install -r requirements.txt`
3. `python3 xosc_dl.py`

##### Manual Download of CLI version:

1. `git clone https://github.com/dhtdht020/osc-dl.git`
2. `cd osc-dl`
2. `pip3 install -r requirements_CLI.txt`
3. `python3 osc-dl.py`

##### USBGecko setup:

See [USBGecko information on WiiBrew](https://wiibrew.org/wiki/USB_Gecko) for device details.

When downloading drivers (if necessary), please use the COM (VCP) drivers instead of the D2XX API.
