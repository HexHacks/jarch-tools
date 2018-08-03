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

class Session:
    def __init__(self, user, token):
        self.user = user
        self.token = token

    def op_key(self):
        return 'OP_SESSION_{}'.format(self.user)

    def environment_enable(self):
        os.environ[self.op_key()] = self.token


def remote_touch_session(user):
    '''
        Use the utility 'op' to login to a given user.
        This works by setting an environment variable, returned by the 'op'.
        This session will hence be active during the runtime of this application.
    '''
    encoding = sys.stdout.encoding
    byte_str = sp.check_output(['op', 'signin', user, '--output=raw'])
    decoded = byte_str.decode(encoding)

    # Remove newline
    decoded = decoded[:len(decoded) - 1]

    return Session(user, decoded)

def login(user):
    session = remote_touch_session(user)
    session.environment_enable()
