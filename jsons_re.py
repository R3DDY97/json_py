#!/usr/bin/env python3
'''converts JSON into python objects'''

import string
import re
import os

# DIGITS = set(string.digits)
# DIGITS_ = set(string.digits).union({"-"})
# FULL_DIGITS = set(string.digits).union({"-", "+", ".", "E", "e"})
# PRINTABLES = set(string.printable).union({'\b', '\f'})
WHITESPACES = set(string.whitespace)


def bool_parser(json_str):
    if json_str[:4] == 'true':
        return (True, json_str[4:])
    elif json_str[:5] == 'false':
        return (False, json_str[5:])
    return None


def null_parser(json_str):
    if json_str[:4] == 'null':
        return (None, json_str[4:])
    return None


def space_parser(json_str) :
    space_match = re.match(r'\s*', json_str)
    if space_match:
        return space_match.group(), json_str[space_match.end():]
    return ("", json_str)
#
def comma_parser(json_str):
    if json_str[0] == ",":
        return (json_str[0], json_str[1:])
    return None


def space_comma_parser(json_str):
    sp_comma_match = re.match(r'\s*,\s*', json_str)
    if sp_comma_match:
        return sp_comma_match.group(), json_str[sp_comma_match.end():]
    return None



def space_colon_parser(json_str):
    sp_colon_match = re.match(r'\s*:\s*', json_str)
    if sp_colon_match:
        return sp_colon_match.group(), json_str[sp_colon_match.end():]
    return None

def string_parser(json_str): # need to clean n fix

    str_match = re.match(r'"[^"]*"', json_str)
    if  str_match:
        return str_match.group(), json_str[str_match.end():]
    return None


def num_parser(json_str):

    # re -- num = re.match(r'-?[1-9]?[0-9]+\.?[0-9]+([eE][+-]?)?[0-9]+', number)
    #re.end()
    # final - '-?[1-9]?[0-9]+\.?[0-9]+([eE]-|[eE]\+|[Ee])?[0-9]+'

    pattern = r'-?[1-9]?[0-9]+\.?[0-9]+([eE]-|[eE]\+|[Ee])?[0-9]+'
    int_match = re.match(pattern, json_str)
    if  int_match:
        return int_match.group(), json_str[int_match.end():]
    return None


def array_parser(json_str):
    if json_str[0] == "[":
        array_asList = []
        json_str = json_str[1:]
    else:
        return None

    if space_parser(json_str):
        _, json_str = space_parser(json_str)

    while json_str[0] != "]":
        parser_output = value_parser(json_str)
        if parser_output:
            value, json_str = parser_output
            array_asList.append(value)
        else:
            break

        if space_parser(json_str):
            _, json_str = space_parser(json_str)

        if json_str[0] != "]" and json_str[0] == ",":
            # _, json_str = comma_parser(json_str)
            _, json_str = ",", json_str[1:]
        else:
            return None
    return (array_asList, json_str)

def object_parser(json_str):
    if json_str[0] == "{":
        object_as_dict = {}
        json_str = json_str[1:]
    else:
        return None

    while json_str[0] != "}":
        if space_parser(json_str):
            _, json_str = space_parser(json_str)

        if string_parser(json_str):
            key, json_str = string_parser(json_str)
        else:
            return None

        if space_colon_parser(json_str):
            _, json_str = space_colon_parser(json_str)
        else:
            return None

        if value_parser(json_str):
            value, json_str = value_parser(json_str)
            object_as_dict[key] = value
        else:
            return None     ## value can  be none ?

        if space_parser(json_str):
            _, json_str = space_parser(json_str)

        if json_str[0] != "}" and json_str[0] == ",":
            _, json_str = ",", json_str[1:]
        else:
            return None
    return (object_as_dict, json_str)




def value_parser(json_str):
    if space_parser(json_str):
        _, json_str = space_parser(json_str)

    parsers = [bool_parser, null_parser, num_parser,
               string_parser, array_parser, object_parser]

    for parser in parsers:
        result = parser(json_str)
        if result:
            return result


# def main():
#     os.system("clear||cls")
#     argument = os.sys.argv[1]
#     if os.path.isfile(argument):
#         json_str = ""
#         with open(os.path.abspath(argument), "r") as json_file:
#             for line in json_file:
#                 json_str += line
#     json_str = json_str.strip()
#     final_output = value_parser(json_str)
#     print(final_output)
#
# if __name__ == '__main__':
#     main()
