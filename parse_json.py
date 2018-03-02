#!/usr/bin/env python3
'''converts JSON into python objects'''

import os
import jsons


def load(jsfile):
    '''runs json parser from input json file'''
    # jsfile = os.path.abspath(os.sys.argv[1])
    if not os.path.isfile(os.path.abspath(jsfile)):
        print("\nCant find the file\n")
        return None
    json_str = ''
    with open(jsfile, "r") as json_content:
        for line in json_content:
            json_str += line
    parser_ouput = jsons.value_parser(json_str)[0]
    return parser_ouput


def loads(json_string):
    '''directly parses JSON input string'''
    parser_ouput = jsons.value_parser(json_string)[0]
    return parser_ouput
