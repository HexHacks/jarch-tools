#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, tempfile

class Tempfile(object):

    def __init__(self, on_open, on_close):
        self.on_open = on_open
        self.on_close = on_close

    def __enter__(self):
        # TODO: investigate this call
        self.path = tempfile.mkstemp()[1]
        self.tmp_file = open(self.path, 'w')
        self.on_open(self.tmp_file)

    def __exit__(self, type, value, traceback):
        # TODO: Both calls needed?
        self.tmp_file.flush()
        self.tmp_file.close()
        self.on_close(self.path)

def set_stdout(file):
    sys.stdout = file

def path_to_less_reset_stdout(path):
    p = subprocess.Popen(['less', path], stdin=subprocess.PIPE)
    p.communicate()
    sys.stdout = sys.__stdout__

def stdout_to_less():
    ''' Use this like so:

        with stdout_to_less():
            print('This string goes to pager')
    '''
    return Tempfile(set_stdout, path_to_less_reset_stdout)

