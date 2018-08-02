#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

    This is a wrapper tool for the 1password-cli, 'op'.
    The raw utility returns json values and loads of
    unintresteing data for regular day-to-day usage.

'''

import os
import argparse
import subprocess as sp
import json

from util import stdout_to_less

from session import login

VERBOSE = False

def log(msg):
    '''
        Log a message iff verbose argument set
    '''
    if VERBOSE:
        print(msg)

def find_subdicts(json_obj, containing=None):
    ''' Trim any non-dict type objects and optionally
        look for a specific container.
    '''
    log("find_subdicts(containing=\'{}\')".format(containing))
    out = []
    for _k in json_obj:
        obj = _k
        if isinstance(json_obj, dict):
            obj = json_obj[_k]

        if isinstance(obj, dict) or isinstance(obj, list):
            if containing is None or containing in obj:
                out.append(obj)

    log("Found {}".format(str(len(out))))
    return out

def get_interesting_values(fields_obj, keys_of_interest):
    ''' Given a 'fields'-dict of keys ('name') and values ('value').
        For example:
            >>> parent = {
                    'fields': { {'name':'Jacob', 'value': True},
                    {'uninteresting':False, 'container':True}
                }
            >>> get_interesting_values(parent['fields'])
            {'name':'Jacob', 'value': True}

    '''
    log('get_interesting_values()')

    dict_key = 'name'
    dict_val = 'value'
    out = {}
    for _o in fields_obj:

        if dict_key in _o and dict_val in _o:
            name = _o[dict_key]
            value = _o[dict_val]
            log("Found named field: {} = {}".format(name, value))
            if name in keys_of_interest:
                out[name] = value
    return out


def fetch_op_item(item_name, keys_of_interest):
    ''' Given an item name, find it in the 'op'-storage and interpret
    '''
    log('')
    log("--> op get item " + item_name)
    output = sp.check_output(['op', 'get', 'item', item_name])

    json_obj = json.loads(output)

    subdict = find_subdicts(json_obj)
    fields = find_subdicts(subdict, 'fields')[0]['fields']

    return get_interesting_values(fields, keys_of_interest)

def fetch_op_list_all(keys_of_interest):
   ''' List all items and return keys of interest
   '''
   log('')
   log('--> op list items')
   output = sp.check_output(['op', 'list', 'items'])

   json_obj = json.loads(output)
   return json_obj


def print_dict(d):
    for _k, _v in d.items():
        print("{}: {}".format(_k, _v))

KEYS_OF_INTEREST = {
    'username',
    'username_or_email',
    'user[password]',
    'password'
}

def user_get(args):
    out = fetch_op_item(args.item, KEYS_OF_INTEREST)
    print_dict(out)

def user_list(args):
    out = fetch_op_list_all(KEYS_OF_INTEREST)

    with stdout_to_less():
        print(json.dumps(out, indent=4, sort_keys=True))


def main():
    ''' Parse and execute user desired functions
    '''
    global VERBOSE

    parser = argparse.ArgumentParser(
            description='Wrapper around the op (1password) utility'
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print out debug information.')

    subparsers = parser.add_subparsers(help='Sub command options')

    # peyop list
    list_parse = subparsers.add_parser('list', description='List all items')
    list_parse.set_defaults(user_func=user_list)

    # peyop get [item]
    get_parse = subparsers.add_parser('get', description='Get a particular item')
    get_parse.add_argument('item', type=str,
                        help='An item to search for in the vault.')
    get_parse.set_defaults(user_func=user_get)

    parser.add_argument('user', type=str,
                        help='1password user name.')
    # Do the parsing
    args = parser.parse_args()

    VERBOSE = args.verbose

    # All commands require us to do a login
    login(args.user)

    args.user_func(args)

if __name__ == "__main__":
    main()
