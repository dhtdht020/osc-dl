import re

from jsonpath_ng import parse


# Parse json with a jsonpath expression
def parse_json_expression(json, expression):
    json_expression = parse(expression)
    json_thing = json_expression.find(json)

    return json_thing


# Escape ansi from stdout
def escape_ansi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)
