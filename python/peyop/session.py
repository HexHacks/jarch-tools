#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess as sp
import sys
import datetime as dt

'''
    This file handles the login procedure.

    TODO:
        * Update $XDG_DATA_HOME/peyop/session
'''

class Session:
    def __init__(self, user, token = None, valid_until = None):
        self.user = user
        self.token = token
        self.valid_until = valid_until
        # Needs refresh every 30 mins.
        # (Might change, read this on the agile bites forum)
        self.refresh_interval = dt.timedelta(0, 60 * 30, 0)

    def valid(self):
        ''' Returns if this session is still valid
        >>> s = Session('anv', 'los')
        >>> s.valid()
        True

        >>> s = Session('a', 'b', dt.datetime(1, 1, 1))
        >>> s.valid()
        False

        >>> tomorrow = dt.datetime.now() + dt.timedelta(1, 0, 0)
        >>> s = Session('a', 'b', tomorrow)
        >>> s.valid()
        True

        >>> yesterday = dt.datetime.now() - dt.timedelta(1, 0, 0)
        >>> s = Session('a', 'b', yesterday)
        >>> s.valid()
        False

        # A session with no user or token is never valid
        >>> s = Session(None, 'b', tomorrow)
        >>> s.valid()
        False

        >>> s = Session('a', None, tomorrow)
        >>> s.valid()
        False
        '''
        if self.user is None or self.token is None:
            return False

        if self.valid_until is None:
            return True

        now = dt.datetime.now()
        return now <= self.valid_until

    def validate(self):
        if self.valid():
            return

        self.remote_touch_token()
        self.touch_timestamp()

        if not self.valid():
            raise Exception('Validate did not succeed in validating')

    def op_key(self):
        return 'OP_SESSION_{}'.format(self.user)

    def set_active(self):
        if not self.valid():
            raise Exception('Can not activate non valid session')

        os.environ[self.op_key()] = self.token

    def touch_timestamp(self):
        '''
        >>> s = Session('a', 'b', dt.datetime(1, 1, 1))
        >>> s.touch_timestamp()
        >>> s.valid()
        True

        '''
        self.valid_until = dt.datetime.now() + self.refresh_interval

    def remote_touch_token(self):
        '''
        Use the utility 'op' to login to a given user.
        This works by setting an environment variable, returned by the 'op'.
        This session will hence be active during the runtime of this application.

        Currently the we use --output=raw, which gives only the token.
        We, as of now, make the assumption that we know the environment
        format.
        '''
        if self.user is None:
            raise Exception('Session needs user info')

        encoding = sys.stdout.encoding
        byte_str = sp.check_output(['op', 'signin', self.user, '--output=raw'])
        decoded = byte_str.decode(encoding)

        # Remove newline
        decoded = decoded[:len(decoded) - 1]

        self.token = decoded

def login(user):
    session = Session(user)
    session.validate()
    session.set_active()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
