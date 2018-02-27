#!/usr/bin/env python3
'''converts JSON into python objects'''

import string

DIGITS = set(string.digits)
DIGITS_ = set(string.digits).union({"-"})
FULL_DIGITS = set(string.digits).union({"-", "+", ".", "E", "e"})
PRINTABLES = set(string.printable).difference({"\\", '"'})
WHITESPACES = set(string.whitespace)


def bool_parser(json_str):
    if json_str[:4] == 'true':
        return (True, json_str[4:])
    elif json_str[:5] == 'false':
        return (False, json_str[5:])


def null_parser(json_str):
    if json_str[:4] == 'null':
        return (None, json_str[4:])


def space_parser(json_str) :
    index = 0
    if json_str[0] != " ":
        return None
    while json_str[index] == " ":
        index += 1
    return (" "*index, json_str[index:])
#
def comma_parser(json_str):
    if json_str[0] == ",":
        return (json_str[0], json_str[1:])
    return None


def space_comma_parser(json_str):
    index = 0
    total_consumed = ""

    while json_str[index] in WHITESPACES:
        total_consumed += json_str[index]
        index += 1
    if json_str[index] == ',':
        total_consumed += ","
        index += 1
    else:
        return None

    while json_str[index] in WHITESPACES:
        total_consumed += json_str[index]
        index += 1
    return (total_consumed, json_str[index:])


def space_colon_parser(json_str):
    index = 0
    total_consumed = ""

    while json_str[index] in WHITESPACES:
        total_consumed += json_str[index]
        index += 1

    if json_str[index] == ':':
        total_consumed += ":"
        index += 1
    else:
        return None

    while json_str[index] in WHITESPACES:
        total_consumed += json_str[index]
        index += 1
    return (total_consumed, json_str[index:])

def string_parser(json_str):
    index = 0
    if json_str[0] != '"':
        return None
    index += 1
    while json_str[index] != '"':
        if json_str[index] in PRINTABLES:
            index += 1
            continue
        if json_str[index] == '\\' and json_str[index+1]  in '\\/"':
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
        if json_str[:3] == "-0.":
            index += 3
            has_dot = True
        else:
            index += 1
    elif json_str[:2] == "0.":
        index += 2
        has_dot = True


    while index < len(json_str) and json_str[index] in FULL_DIGITS:
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

    return (json_str[:index], json_str[index:])


def array_parser(json_str):
    if json_str[0] == "[":
        array_asList = []
        json_str = json_str[1:]
    else:
        return None

    if whitespace_parser(json_str):
        consumed, json_str = whitespace_parser(json_str)

    while json_str[0] != "]":
        parser_output = value_parser(json_str)
        if parser_output:
            value, json_str = parser_output
            array_asList.append(value)
        else:
            break

        if whitespace_parser(json_str):
            _, json_str = whitespace_parser(json_str)

        if json_str[0] == "]":
            continue
        elif json_str[0] == ",":
            _, json_str = comma_parser(json_str)
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
        if whitespace_parser(json_str):
            _, json_str = whitespace_parser(json_str)
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
            return None

        if whitespace_parser(json_str):
            _, json_str = whitespace_parser(json_str)

        if json_str[0] == "}":
            break
        elif json_str[0] == ",":
            _, json_str = comma_parser(json_str)
        else:
            return None
    return (object_as_dict, json_str)


def whitespace_parser(json_str):
    index = 0
    if json_str[index] in WHITESPACES:
        index += 1
    else:
        return None
    while json_str[index] in WHITESPACES:
        index += 1
    return (json_str[:index], json_str[index:])



def value_parser(json_str):
    if whitespace_parser(json_str):
        _, json_str = whitespace_parser(json_str)

    parsers = [bool_parser, null_parser, num_parser,
               string_parser, array_parser, object_parser]

    for parser in parsers:
        result = parser(json_str)
        if result:
            return result
