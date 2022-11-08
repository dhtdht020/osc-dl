import re
import zipfile
import copy
import os
import zlib
import socket
import struct

IP_REGEX = re.compile(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$|^(?:(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){6})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:::(?:(?:(?:[0-9a-fA-F]{1,4})):){5})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){4})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,1}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){3})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,2}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){2})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,3}(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:[0-9a-fA-F]{1,4})):)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,4}(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,5}(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,6}(?:(?:[0-9a-fA-F]{1,4})))?::))))$")

# WiiLoad
WIILOAD_VER_MAJOR = 0
WIILOAD_VER_MINOR = 5
CHUNK_SIZE = 1024


def validate_ip_regex(ip):
    # check IP address against regex
    return IP_REGEX.match(ip)


def organize_zip(zipped_app, zip_buf):
    zip_file = zipfile.ZipFile(zipped_app, mode='r')
    app_infolist = zip_file.infolist()

    # Our zip file should only contain one directory with the app data in it,
    # but the downloaded file contains an apps/ directory. We're removing that here.
    app_zip = zipfile.ZipFile(zip_buf, mode='w', compression=zipfile.ZIP_DEFLATED)

    # copy over all files
    for info in app_infolist:
        new_path = info.filename.replace('apps/', '')
        if not new_path:
            continue

        # we need to copy over the member info manually because
        # python's zipfile implementation sucks and
        # the HBC is very insecure about it.
        new_info = copy.copy(info)
        new_info.filename = new_path

        if new_info.filename[-1] in ('/', '\\'):  # directory
            continue

        with zip_file.open(info.filename, 'r') as file:
            data = file.read()

        app_zip.writestr(new_path, data)

    # cleanup
    zipped_app.close()
    zip_file.close()
    app_zip.close()


def prepare(zip_buf):
    # preparing
    zip_buf.seek(0, os.SEEK_END)
    file_size = zip_buf.tell()
    zip_buf.seek(0)

    c_data = zlib.compress((zip_buf.read()))
    compressed_size = len(c_data)
    chunks = [c_data[i:i + CHUNK_SIZE] for i in range(0, compressed_size, CHUNK_SIZE)]

    return file_size, compressed_size, chunks
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
        # progress = round(chunk_num / len(chunks) * 50) + 50
        # self.ui.progressBar.setValue(progress)

    file_name = f'{app_name}.zip'
    conn.send(bytes(file_name, 'utf-8') + b'\x00')
