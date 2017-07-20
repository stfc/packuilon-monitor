#!/usr/bin/env python2

import os


def get_log_root_dir():
    return "/home/htv52873/code/packuilon-monitor/test/log"


def get_log(log_name):
    '''Retrieve the contents of a log, given its filename.'''
    with open(os.path.join(get_log_root_dir(), log_name), 'r') as f:
        return f.read()


def log_files(dir):
    '''Return a list of files/dirs in a directory, with full paths.

    This is as opposed to os.listdir(), which gives you the relative paths of
    the files.
    '''
    return map(lambda f: os.path.join(dir, f),
               os.listdir(dir))
