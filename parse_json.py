#!/usr/bin/env python3
'''converts JSON into python objects'''

import os
from pprint import pprint
import jsons



def load():
    '''runs json parser from input json file'''
    jsfile = os.path.abspath(os.sys.argv[1])
    if os.path.isfile(os.path.abspath(jsfile)):
        json_str = ''
        with open(jsfile, "r") as json_content:
            for line in json_content:
                json_str += line
    parser_ouput = jsons.value_parser(json_str)[0]
    pprint(parser_ouput)
    return parser_ouput


def loads(json_str):
    '''directly parses JSON input string'''
    parser_ouput = jsons.value_parser(json_str)[0]
    pprint(parser_ouput)
    return parser_ouput


if __name__ == '__main__':
    load()