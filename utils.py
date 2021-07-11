import re

# Escape ansi from stdout
import sys


def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def is_test(name):
    if len(sys.argv) > 1 and (sys.argv[1] == name):
        return True
    else:
        return False
