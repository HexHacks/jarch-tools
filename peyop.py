#!/usr/bin/python3

'''

    This is a wrapper tool for the 1password-cli, 'op'.
    The raw utility returns json values and loads of
    unintresteing data for regular day-to-day usage.

'''

import os
import argparse
import subprocess as sp
import json

PARSER = argparse.ArgumentParser(description='Wrapper around the op (1password) utility')
PARSER.add_argument('user', type=str,
                    help='1password user name.')
PARSER.add_argument('item', type=str,
                    help='An item to search for in the vault.')

#PARSER.add_argument('-c', '--no-clipboard', action='store_true',
#                   help='Don\'t copy the output to the clipboard.')

PARSER.add_argument('-v', '--verbose', action='store_true',
                    help='Print out debug information.')

ARGS = PARSER.parse_args()

def log(msg):
    '''
        Log a message iff verbose argument set
    '''
    if ARGS.verbose:
        print(msg)

def remove_newline(str_):
    '''
        The utility 'op' seems to give us weird newlines (probably for bash?),
        remove these.
    '''
    news = ['\n', '\\n', '\r', '\\r']
    out = str_

    for _n in news:
        out = out.replace(_n, ' ')
    return out

def login(user):
    '''
        Use the utility 'op' to login to a given user.
        This works by setting an environment variable, returned by the 'op'.
        This session will hence be active during the runtime of this application.
    '''
    log("--> op signin " + user)
    output = str(sp.check_output(['op', 'signin', user]))

    log("Output:")
    log(output)

    output = remove_newline(output)
    #sp.check_call(['eval', '$(op signin {})'.format(user)])

    log("")
    exports = [x for x in output.split() if x.startswith('OP_SESSION')]
    for e in exports:
        epos = e.find('=')
        key = e[:epos]
        val = e[epos:].strip(' =\"')

        log('env[\'{}\'] = {}'.format(key, val))
        os.environ[key] = val

def find_subdicts(json_obj, containing=None):
    '''
        Trim any non-dict type objects and optionally look for a specific container.
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

def get_interesting_values(fields_obj):
    '''
        Given a 'fields'-dict of keys ('name') and values ('value').
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
    keys_of_interest = {'username_or_email', 'password'}
    out = {}
    for _o in fields_obj:

        if dict_key in _o and dict_val in _o:
            name = _o[dict_key]
            value = _o[dict_val]
            log("Found named field: {} = {}".format(name, value))
            if name in keys_of_interest:
                out[name] = value
    return out


def get_values(item_name):
    '''
        Given an item name, find it in the 'op'-storage and interpret
    '''
    log('')
    log("--> op get item " + item_name)
    output = sp.check_output(['op', 'get', 'item', item_name])

    json_obj = json.loads(output)

    subdict = find_subdicts(json_obj)
    fields = find_subdicts(subdict, 'fields')[0]['fields']

    return get_interesting_values(fields)

login(ARGS.user)

if ARGS.item is not None:
    item = get_values(ARGS.item)
    for _k, _v in item.items():
        print("{}: {}".format(_k, _v))

#if not ARGS.no_clipboard:
#    print('CLIPBOARD NOT IMPLEMENTED.')
