#!/usr/bin/env python3
'''converts JSON into python objects'''

import string
import os
from pprint import pprint

DIGITS = set(string.digits)
DIGITS_ = set(string.digits).union({"-"})
FULL_DIGITS = set(string.digits).union({"-", "+", ".", "E", "e"})
WHITESPACES = set(string.whitespace)


def bool_parser(json_str):
    '''parses boolean obj in JSON'''
    if json_str[:4] == 'true':
        return (True, json_str[4:])
    elif json_str[:5] == 'false':
        return (False, json_str[5:])
    return None


def null_parser(json_str):
    if json_str[:4] == 'null':
        return (None, json_str[4:])
    return None

def whitespace_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[:index], json_str[index:]

def space_comma_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    if json_str[index] == ',':
        index += 1
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[:index], json_str[index:]


def space_colon_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    if json_str[index] == ':':
        index += 1
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[:index], json_str[index:]

def string_parser(json_str):
    index = 0
    if json_str[0] != '"':
        return None
    index += 1
    while json_str[index] != '"' or json_str[index-1]+json_str[index] == '\\"':
        if ord(json_str[index]) not in range(65536):
            return None
        index += 1
    return (json_str[1:index], json_str[index+1:])

def num_parser(json_str):
    index = 0
    has_dot = False
    has_e = False
    has_minus = False

    if json_str[index] not in DIGITS_:
        return None
    if json_str[index:2] == "00" or json_str[index:3] == "-00":
        return None

    if json_str[0] == "-":
        has_minus = True
        index += 1
        if json_str[:3] == "-0.":
            index += 2
            has_dot = True
    elif json_str[:2] == "0.":
        index += 2
        has_dot = True

    while json_str[index] in FULL_DIGITS and not has_e:
        if json_str[index] == "-" and not has_minus:
            has_minus = True

        elif json_str[index].lower() == "e":
            has_e = True
            if json_str[index+1] in "+-":
                index += 1

        elif json_str[index] == "." and not has_dot:
            has_dot = True
        index += 1

    number = json_str[:index]
    try:
        if isinstance(int(number), int):
            return (int(number), json_str[index:])
    except ValueError:
        return (float(number), json_str[index:])

def array_parser(json_str):
    array_list = []
    if json_str[0] == "[" and json_str[1] == "]":
        return (array_list, json_str[2:])
    elif json_str[0] == "[":
        json_str = json_str[1:]
    else:
        return None

    _, json_str = whitespace_parser(json_str)
    while json_str[0] != "]":
        value, json_str = value_parser(json_str)
        array_list.append(value)
        _, json_str = space_comma_parser(json_str)
    return (array_list, json_str[1:])

def object_parser(json_str):
    object_as_dict = {}
    if json_str[0] == "{" and json_str[1] == "}":
        return (object_as_dict, json_str[2:])
    if json_str[0] == "{":
        json_str = json_str[1:]
    else:
        return None

    _, json_str = whitespace_parser(json_str)
    while json_str[0] != "}":
        key, json_str = string_parser(json_str)
        _, json_str = space_colon_parser(json_str)
        object_as_dict[key], json_str = value_parser(json_str)
        _, json_str = space_comma_parser(json_str)
    return (object_as_dict, json_str[1:])


def value_parser(json_str):
    ''' main function which calls the other subparser functions taking input JSON string'''

    _, json_str = whitespace_parser(json_str)
    parsers = [bool_parser, null_parser, num_parser,
               string_parser, array_parser, object_parser]
    for parser in parsers:
        result = parser(json_str)
        if result:
            return result
    return None


def main():
    '''runs json parser from input json file'''
    jsfile = os.path.abspath(os.sys.argv[1])
    if not os.path.isfile(os.path.abspath(jsfile)):
        print("\nCant find the file\n")
        os.sys.exit(1)
    json_str = ''
    with open(jsfile, "r") as json_content:
        for line in json_content:
            json_str += line
    parser_ouput = value_parser(json_str)[0]
    pprint(parser_ouput)
    return parser_ouput

if __name__ == '__main__':
    main()
