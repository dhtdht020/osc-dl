import zipfile
import copy
import os
import zlib
import socket
import struct
import ipaddress

# WiiLoad
WIILOAD_VER_MAJOR = 0
WIILOAD_VER_MINOR = 5
CHUNK_SIZE = 1024
DATASENT = True


def validate_ip_regex(ip):
    # check IP address against regex
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False
    return True


def organize_zip(zipped_app, zip_buf):
    zip_file = zipfile.ZipFile(zipped_app, mode='r')
    app_infolist = zip_file.infolist()

    # Our zip file should only contain one directory with the app data in it,
    # but it will be kept, as long is it's relative to the root of the SD/USB. 
    # This creates a zip file based on relative directories to extract all files.
    app_zip = zipfile.ZipFile(zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED)

    # Zip manipulation time.
    # First we need the directory name of the app.
    dirname = ""
    appname = ""
    for info in app_infolist:
        if 'apps/' in info.filename and info.filename != 'apps/':
            appname = info.filename.split("/")[1]
            dirname = appname+"/"
            break

    # Copy over all files
    # In HBC, the app is directly written at the apps directory.
    # The app's name MUST be the first directory name in apps.
    # HBC will check for consistant directory names, 
    # if one does not match, it gives the "Unusable zip" error.
    # This means we need the app's directory first.
    boot_dol_found = False
    for info in app_infolist:
        if 'apps/' in info.filename:
            new_path = info.filename.replace('apps/', '')
        else:
            # However, HBC does not check for relative directories.
            # By stepping back two directories, we are at the root of the SD/USB.
            new_path = dirname + "../../" + info.filename 
            # Just in case there is a rogue README file.
            if f"{dirname}../../read".upper() in new_path.upper():
                READMEFile = new_path.split(".")[-2]
                new_path = new_path.replace(READMEFile,f'{READMEFile}_{appname}')

        # Bug fix: Skip adding 'boot.elf' if 'boot.dol' is present
        # This is done because HBC only supports receiving one or the other.
        # boot.dol has priority as the preferred format for distribution.
        if 'boot.elf' in new_path and boot_dol_found:
            continue
        if 'boot.dol' in new_path:
            boot_dol_found = True
                
        if not new_path:
            continue

        # we need to copy over the member info manually because
        # python's zipfile implementation sucks and
        # the HBC is very insecure about it.
        new_info = copy.copy(info)
        new_info.filename = new_path

        with zip_file.open(info.filename, 'r') as file:
            data = file.read()

        app_zip.writestr(new_path, data)

    # Finally, if a directory is empty, HBC will not write it.
    # So, this adds a dot file to all directories, regardless of contents.
    # HBC will delete that file, but not the directory.
    # Addtionally, if a file is 0 bytes, add something to it.
    # NOTE: HBC will delete all 0 byte files and dot files.
    for x in app_zip.filelist:
        if x.is_dir():
            with app_zip.open(x.filename+'._OSCDL', 'w') as temp: 
                temp.write("This file can be deleted.".encode("utf-8"))
        elif x.file_size == 0:
            with app_zip.open(x.filename, 'w') as temp: 
                temp.write('.'.encode("utf-8"))
    # cleanup
    zipped_app.close()
    zip_file.close()
    app_zip.close()

    # DEBUG: Save the organized zip to a file
    with open("debug.zip", 'wb') as f_debug:
        f_debug.write(zip_buf.getvalue())  # Save the content of zip_buf to file


def prepare(zip_buf):
    # preparing
    zip_buf.seek(0, os.SEEK_END)
    file_size = zip_buf.tell()
    zip_buf.seek(0)

    c_data = zlib.compress((zip_buf.read()))
    compressed_size = len(c_data)
    chunks = [c_data[i:i + CHUNK_SIZE] for i in range(0, compressed_size, CHUNK_SIZE)]

    return file_size, compressed_size, chunks, c_data
    # obtain returned values outside with:
    # file_size = prep[0]
    # compressed_size = prep[1]
    # chunks = prep[2]


def connect(ip):
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.settimeout(2)
    conn.connect((ip, 4299))
    return conn


def handshake(conn, compressed_size, file_size):
    # handshake, all data types are unsigned
    conn.send(b'HAXX')
    conn.send(struct.pack('B', WIILOAD_VER_MAJOR))  # char
    conn.send(struct.pack('B', WIILOAD_VER_MINOR))  # char
    conn.send(struct.pack('>H', 0))  # big endian short
    conn.send(struct.pack('>L', compressed_size))  # big endian long
    conn.send(struct.pack('>L', file_size))  # big endian long


def send(chunks, conn, app_name):
    chunk_num = 1
    for chunk in chunks:
        conn.send(chunk)

        chunk_num += 1

    file_name = f'{app_name}.zip'
    conn.send(bytes(file_name, 'utf-8') + b'\x00')


def send_gecko(data, conn):
    try:
        conn.send(data)
    except Exception as e:
        print('Error while connecting to the HBC. Close any dialogs on HBC and try again.')

        print(f'Exception: {e}')
        print('Error: Could not connect to the Homebrew Channel. :(')

        # delete application zip file
        conn.close()
        exit(1)
