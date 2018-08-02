#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp

'''
    This file handles the login procedure.

    TODO:
        * Update $XDG_DATA_HOME/peyop/session
'''

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
    output = str(sp.check_output(['op', 'signin', user]))

    output = remove_newline(output)
    #sp.check_call(['eval', '$(op signin {})'.format(user)])

    exports = [x for x in output.split() if x.startswith('OP_SESSION')]
    for e in exports:
        epos = e.find('=')
        key = e[:epos]
        val = e[epos:].strip(' =\"')

        os.environ[key] = val
