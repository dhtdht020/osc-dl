import re

IP_REGEX = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


def validate_ip_regex(ip):
    ip_match = IP_REGEX.match(ip)
    return ip_match
