#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp
import sys

'''
    This file handles the login procedure.

    TODO:
        * Update $XDG_DATA_HOME/peyop/session
'''

def token_key(user):
    return 'OP_SESSION_{}'.format(user)

def remote_fetch_token(user):
    '''
        Use the utility 'op' to login to a given user.
        This works by setting an environment variable, returned by the 'op'.
        This session will hence be active during the runtime of this application.
    '''
    encoding = sys.stdout.encoding
    byte_str = sp.check_output(['op', 'signin', user, '--output=raw'])
    decoded = byte_str.decode(encoding)
    return decoded[:len(decoded) - 1] # Remove newline

def login(user):
    token = remote_fetch_token(user)
    key = token_key(user)
    os.environ[key] = token
