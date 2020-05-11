from shutil import copyfile
import os
import subprocess
from sys import exit

# Initialize state
failed = False

FAIL_get_test = False
FAIL_query_test = False

# Check Operating System
if os.name == 'nt':
    # Windows
    print("[INFO] Running on Windows")
    os_name = "NT"
else:
    # other (unix)
    print("[INFO] Running on Linux (UNIX)")
    os_name = "UNIX"

if os_name is "NT":
    filename = "osc-dl.exe"
else:
    filename = "osc-dl"


# Copy binary to tests dir
print("Moving osc-dl to tests directory..")
copyfile("../dist/" + filename, "./" + filename)


# Check if server is online
# Not implemented


# Check if get works
print("\n\n[INFO] GET TEST: Trying to get -n WiiVNC..")
get_test = subprocess.Popen(filename + " get -n WiiVNC", stdin=subprocess.PIPE, shell=True)
get_test.stdin.write(b"y\n")
get_test.stdin.flush()
stdout, stderr = get_test.communicate()
if get_test.returncode != 0:
    failed = True
    FAIL_get_test = True

    print("[FAILURE] GET TEST: Failed, continuing.")
else:
    print("[SUCCESS] GET TEST: Passed, continuing.")


# Check if query works
print("\n\n[INFO] QUERY TEST: Trying to query -n WiiVNC..")
query_test = subprocess.Popen(filename + " query -n WiiVNC", stdin=subprocess.PIPE, shell=True)
query_test.stdin.write(b"y\n")
query_test.stdin.flush()
stdout, stderr = query_test.communicate()
if query_test.returncode != 0:
    failed = True
    FAIL_query_test = True

    print("[FAILURE] QUERY TEST: Failed, continuing.")
else:
    print("[SUCCESS] QUERY TEST: Passed, continuing.")


# Test Summary
print("\n=========== Download Test Summary ===========")
print("FAIL: True                     SUCCESS: False")
print("=============================================")
print("Get Test: " + str(FAIL_get_test))
print("Query Test: " + str(FAIL_query_test))
print("\nConclusion: " + str(failed))
print("=============================================\n")

if failed is True:
    print("Test failed. Returning exit code of 1.")
    exit(1)
else:
    print("Test successful! Returning exit code of 0.")
    exit(0)
