
# Open Shop Channel DL [![Actions Status](https://github.com/dhtdht020/osc-dl/workflows/Build/badge.svg)](https://github.com/dhtdht020/osc-dl/actions) [![Discord Server](https://img.shields.io/discord/426478571389976577.svg)](https://discord.gg/by6mR5N) [![Downloads](https://img.shields.io/github/downloads/dhtdht020/osc-dl/total)](https://github.com/dhtdht020/osc-dl/releases) [![License](https://img.shields.io/badge/Open%20Source-GPL--3.0-lightgrey.svg)](https://github.com/dhtdht020/osc-dl/blob/master/LICENSE)

OSCDL is a cross platform desktop client created by dhtdht020, founder of the Open Shop Channel project, for browsing the Open Shop Channel homebrew repository.

It is built using Python 3 and the Qt framework.

This client provides an easy and intuitive graphical user interface, enabling quick browsing of the homebrew applications library, and remote deployment of apps to the console through the local network or through USB Gecko.

![Preview](https://github.com/dhtdht020/osc-dl/assets/18469146/031856f6-fd3b-4348-869b-2943cee37fd7)

## Installing OSCDL

### Windows

If you are a Windows user, it is recommended to download the latest prebuilt release from
[https://github.com/dhtdht020/osc-dl/releases](https://github.com/dhtdht020/osc-dl/releases)

This release provides a "frozen binary" of the project, sparing you from downloading Python and the project dependencies :)

Alternatively, you can run OSCDL from source (requires **Git** and **Python 3**):

1. `git clone https://github.com/dhtdht020/osc-dl.git`
2. `cd osc-dl`
3. `pip3 install -r requirements.txt`
4. `python3 oscdl.py`

---

### Linux and macOS

Make sure **Python 3.11+** is installed.
On some Linux distributions, you may also need to install `python3-venv`.

1. `git clone https://github.com/dhtdht020/osc-dl.git`
2. `cd osc-dl`
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
   
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
   
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
6. Run OSCDL:
   ```bash
   python oscdl.py
   ```

To deactivate the virtual environment:

```bash
deactivate
```

## USBGecko setup:

See [USBGecko information on WiiBrew](https://wiibrew.org/wiki/USB_Gecko) for device details.

When downloading drivers (if necessary), please use the COM (VCP) drivers instead of the D2XX API.
