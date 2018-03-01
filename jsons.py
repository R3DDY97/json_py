#!/usr/bin/env python3
'''converts JSON into python objects'''

import string
import os
from pprint import pprint

DIGITS = set(string.digits)
DIGITS_ = set(string.digits).union({"-"})
FULL_DIGITS = set(string.digits).union({"-", "+", ".", "E", "e"})
WHITESPACES = set(string.whitespace)
# PRINTABLES = set(string.printable).difference({"\\", '"'})


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


def whitespace_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[index:]

def space_comma_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    if json_str[index] == ',':
        index += 1
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[index:]


def space_colon_parser(json_str):
    index = 0
    while json_str[index] in WHITESPACES:
        index += 1
    if json_str[index] == ':':
        index += 1
    while json_str[index] in WHITESPACES:
        index += 1
    return json_str[index:]

def string_parser(json_str):
    index = 0
    if json_str[0] != '"':
        return None
    index += 1
    while True:
        if json_str[index] == '"' and json_str[index-1]+json_str[index] != '\\"':
            break
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
        if json_str[:3] == "-0.":
            index += 3
            has_dot = True
        else:
            index += 1
    elif json_str[:2] == "0.":
        index += 2
        has_dot = True

    while json_str[index] in FULL_DIGITS:
        if json_str[index] in DIGITS:
            index += 1
        elif json_str[index] == "-":
            if has_minus:
                return None
            else:
                has_minus = True
                index += 1

        elif json_str[index].lower() == "e":
            if has_e:
                return None
            else:
                has_e = True
                if json_str[index+1] in "+-":
                    index += 2
                else:
                    index += 1

        elif json_str[index] == ".":
            if has_dot:
                return None
            elif not has_dot:
                index += 1
                has_dot = True

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

    json_str = whitespace_parser(json_str)

    while json_str[0] != "]":
        parser_output = value_parser(json_str)
        if parser_output:
            value, json_str = parser_output
            array_list.append(value)
        else:
            break

        json_str = whitespace_parser(json_str)

        if json_str[0] == "]":
            break
        elif space_comma_parser(json_str):
            json_str = space_comma_parser(json_str)
    return (array_list, json_str[1:])

def object_parser(json_str):

    object_as_dict = {}

    if json_str[0] == "{" and json_str[1] == "}":
        return (object_as_dict, json_str[2:])
    if json_str[0] == "{":
        json_str = json_str[1:]
    else:
        return None

    while json_str[0] != "}":
        json_str = whitespace_parser(json_str)

        if string_parser(json_str):
            key, json_str = string_parser(json_str)
        else:
            break

        if space_colon_parser(json_str):
            json_str = space_colon_parser(json_str)
        else:
            return None

        if value_parser(json_str):
            value, json_str = value_parser(json_str)
            object_as_dict[key] = value
        else:
            return None

        json_str = whitespace_parser(json_str)

        if json_str[0] == "}":
            break

        elif space_comma_parser(json_str):
            json_str = space_comma_parser(json_str)

    return (object_as_dict, json_str[1:])



def value_parser(json_str):
    ''' main function which calls the other subparser functions taking input JSON string'''

    json_str = whitespace_parser(json_str)

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
    if os.path.isfile(os.path.abspath(jsfile)):
        json_str = ''
        with open(jsfile, "r") as json_content:
            for line in json_content:
                json_str += line
    parser_ouput = value_parser(json_str)[0]
    pprint(parser_ouput)
    return parser_ouput

if __name__ == '__main__':
    main()
