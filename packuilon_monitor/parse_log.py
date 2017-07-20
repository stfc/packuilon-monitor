#!/usr/bin/env python2

import re
import os
from get_log import get_log, log_files, get_log_root_dir
from collections import namedtuple

# The build info is a 5-tuple comprising:
#  1. the name of the build;
#  2. the start time (epoch);
#  3. the build status ('running', 'passed', 'failed')
#  4. the end time (possibly None, if still running);
#  5. the exit code (possibly None).

# NOTE. You can rely on 1--3 being defined.
# If the build is 'running', (4) and (5) will be None.
# If the build has 'failed', (4) *might* be None if the build was cancelled.

BuildInfo = namedtuple('BuildInfo',
                       ('path', 'name', 'start_time', 'status', 'end_time', 'exit_code'))


_finished_line_matcher = re.compile(r'^rabbit2packer: Build finished at (\d+) \(epoch\) with exit code (\d+)$')
_cancelled_line_matcher = re.compile(r'^Cleanly cancelled builds after being interrupted.$')

# FIXME: rewrite to return a dict of information gleaned, then rewrite the
# BuildInfo constructors at the bottom to use `if X in Y: ...` to test the
# presence of keys.
def parse_status_line(line):
    '''Match a line of a build log for finish time and exit code.'''
    m = re.match(_finished_line_matcher, line)
    if m:
        (t, e) = m.group(1,2)
        return (int(t), int(e))
    elif re.match(_cancelled_line_matcher, line):
        return (None, 130) # exit code for ^C
    else:
        return False

_filename_info_matcher = re.compile(r'^([^.]+\.[^.]+)\.json\.(\d+)\.log')
def parse_filename_info(name):
    '''Extract build name and start time from name of log file as a 2-tuple (str, int).'''
    m = re.match(_filename_info_matcher, name)
    if m:
        (n, t) = m.group(1,2)
        return (n, int(t))
    else:
        return False

def get_last_line(filepath):
    y = None
    with open(filepath, 'r') as f:
        while y != '':
            x = y
            y = f.readline()
        return x


def parse_log_info(filename, line):
    name_info = parse_filename_info(filename)
    stat_info = parse_status_line(line)
    if name_info:
        (n, t0) = name_info
        if stat_info:
            (t1, e) = stat_info
            if e == 0:
                return BuildInfo(filename, n, t0, 'passed', t1, e)
            else:
                return BuildInfo(filename, n, t0, 'failed', t1, e) # NOTE: t1 can still be None if build was cancelled.
        else:
            return BuildInfo(filename, n, t0, 'running', None, None)
    else:
        None


def get_log_info(filepath):
    '''Scrape the build info from a named log file as a BuildInfo named tuple.'''
    filename = os.path.basename(filepath)
    last_line = get_last_line(filepath)
    return parse_log_info(filename, last_line)


def get_builds():
    '''Return a list of all the build information given the directory of the logs.'''
    return filter(lambda b: b != None, [get_log_info(log) for log in log_files(get_log_root_dir())])

# run tests
if __name__ == '__main__':
    import doctest
    doctest.testmod()

# NOTE: Doctest views 'foo' and "foo" as different values (possibly because it
# compares values by looking at their `repr'). If you get a failed test like
#     Expected "foo"
#     But got  'foo'
# then just change the quote style in the test.
