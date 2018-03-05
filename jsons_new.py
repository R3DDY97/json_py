#!/usr/bin/env python3
'''converts JSON into python objects'''

import os
from pprint import pprint

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

def string_parser(json_str):
    index = 0
    if json_str[0] == '"':
        index += 1
        while json_str[index] != '"' or json_str[index-1]+json_str[index] == '\\"':
            index += 1
        return (json_str[1:index], json_str[index+1:])
    return None

def num_parser(json_str):
    index, has_dot, has_e = 0, False, False
    if json_str[index] not in "0123456789-":
        return None
    if json_str[0] == "-":
        index += 1
    if json_str[index:2] == "0.":
        index += 2
        has_dot = True

    while json_str[index] in "0123456789eE.":
        if json_str[index].lower() == "e":
            if has_e:
                return None
            elif json_str[index+1] in "+-":
                has_e = True
                index += 1
        elif json_str[index] == ".":
            if not has_dot:
                has_dot = True
            else:
                return None
        index += 1
    number = json_str[:index]
    try:
        if isinstance(int(number), int):
            return (int(number), json_str[index:])
    except ValueError:
        return (float(number), json_str[index:])

def array_parser(json_str):
    array_list = []
    if json_str[0] == "[":
        json_str = json_str[1:].lstrip()
    else:
        return None

    while json_str[0] != "]":
        value_parsed = value_parser(json_str)
        if value_parsed:
            value, json_str = value_parsed[0], value_parsed[1].lstrip()
            array_list.append(value)
        else:
            break
        if json_str[0] == ",":
            if json_str[1:].lstrip()[0] == "]":
                return None
            json_str = json_str[1:].lstrip()
    return (array_list, json_str[1:])

def object_parser(json_str):
    if json_str[0] == "{":
        json_str = json_str[1:].lstrip()
    else:
        return None

    object_as_dict = {}
    while json_str[0] != "}":
        string_parsed = string_parser(json_str)
        if string_parsed:
            key, json_str = string_parsed[0], string_parsed[1].lstrip()
        else:
            break
        if json_str[0] == ":":
            json_str = json_str[1:].lstrip()
            value_parsed = value_parser(json_str)
            if value_parsed:
                object_as_dict[key], json_str = value_parsed[0], value_parsed[1].lstrip()
        else:
            return None
        if json_str[0] == ",":
            if json_str[1:].lstrip()[0] == "}":
                return None
            json_str = json_str[1:].lstrip()
    return (object_as_dict, json_str[1:])

def value_parser(json_str):
    ''' main function which calls the other subparser functions taking input JSON string'''
    json_str = json_str.lstrip()
    parsers = [bool_parser, null_parser, num_parser,
               string_parser, array_parser, object_parser]
    for parser in parsers:
        value_parsed = parser(json_str)
        if value_parsed:
            return value_parsed
    return None


def main():
    '''runs json parser from input json file'''
    jsfile = os.path.abspath(os.sys.argv[1])
    if not os.path.isfile(os.path.abspath(jsfile)):
        print("\n\tCant find the file\n")
        return None
    json_str = ''
    with open(jsfile, "r") as json_content:
        for line in json_content:
            json_str += line

    parsed_json = value_parser(json_str)
    if parsed_json:
        pprint(parsed_json[0])
        return parsed_json[0]
    print("\n\tNot a Valid JSON\n")
    return None

if __name__ == '__main__':
    main()
