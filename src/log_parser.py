#!/usr/bin/env python2

import re
import os
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
                       ('name', 'start_time', 'status', 'end_time', 'exit_code'))

# FIXME: will define this in the main package, not here.
## LOGDIR = '/etc/packer-utils/log/'

_status_line_matcher = re.compile(r'^rabbit2packer: Build finished at (\d+) \(epoch\) with exit code (\d+)$')
_cancelled_line_matcher = re.compile(r'^Cleanly cancelled builds after being iterrupted.$')

def match_status_line(line):
    '''Match a line of a build log for finish time and exit code.

    >>> match_status_line('rabbit2packer: Build finished at 1500000000 (epoch) with exit code 1')
    (1500000000, 1)
    >>> match_status_line('rabbit2packer: Build finished at 42 (epoch) with exit code 0')
    (42, 0)
    >>> match_status_line('rabbit2packer: Build finished at 2000000000000000 (epoch) with exit code 42')
    (2000000000000000, 42)
    >>> match_status_line('hare2packer: Build finished at 1500000000 (epoch) with exit code 1')
    False
    >>> match_status_line('rabbit2packer: Build finished at -99000 (epoch) with exit code 1')
    False
    >>> match_status_line('rabbit2packer: Build finished at 99000 (epoch) with exit code -53')
    False
    '''
    m = re.match(_status_line_matcher, line)
    if m:
        (t, e) = m.group(1,2)
        return (int(t), int(e))
    elif re.match(_cancelled_line_matcher, line):
        return (None, 130) # exit code for ^C
    else:
        return False

_filename_info_matcher = re.compile(r'^([^.]+\.[^.]+)\.json\.(\d+)\.log')
def match_filename_info(name):
    '''Extract build name and start time from name of log file as a 2-tuple (str, int)

    >>> match_filename_info('inventory-sl6x.unmanaged.json.1500000000.log')
    ('inventory-sl6x.unmanaged', 1500000000)
    >>> match_filename_info('freddie.mercury.json.1946.log')
    ('freddie.mercury', 1946)
    >>> match_filename_info('freddie.mercury.json.-1946.log')
    False
    >>> match_filename_info('f.r.e.d.d.i.e.m.e.r.c.u.r.y.json.1946.log')
    False
    >>> match_filename_info('..json..log')
    False
    '''
    m = re.match(_filename_info_matcher, name)
    if m:
        (n, t) = m.group(1,2)
        return (n, int(t))
    else:
        return False

def log_files(dir):
    '''Return a list of files/dirs in a directory, with full paths.

    This is as opposed to os.listdir(), which gives you the relative paths of
    the files.
    '''
    return map(lambda f: os.path.join(dir, f),
               os.listdir(dir))

def get_last_line(filepath):
    y = None
    with open(filepath, 'r') as f:
        while y != '':
            x = y
            y = f.readline()
        return x

def get_log_info(filepath):
    '''Scrape the build info from a named log file as a BuildInfo named tuple.

    The following examples make use of the stubbed log files in test/log.

    >>> get_log_info('./test/log/inventory-sl6x.managed.json.1499871318.log')
    BuildInfo(name='inventory-sl6x.managed', start_time=1499871318, status='passed', end_time=1499872060, exit_code=0)
    '''
    filename = os.path.basename(filepath)
    name_info = match_filename_info(filename)
    stat_info = match_status_line(get_last_line(filepath))
    if name_info:
        (n, t0) = name_info
        if stat_info:
            (t1, e) = stat_info
            if e == 0:
                return BuildInfo(n, t0, 'passed', t1, e)
            else:
                return BuildInfo(n, t0, 'failed', t1, e) # NOTE: t1 can still be None if build was cancelled.
        else:
            return BuildInfo(n, t0, 'running', None, None)
    else:
        raise Exception("Couldn't parse \"%s\" for build name and start time info." % filename)

def get_builds(log_root):
    '''Return a list of all the build information given the directory of the logs.'''
    return [get_log_info(log) for log in log_files(log_root)]

# run tests
if __name__ == '__main__':
    import doctest
    doctest.testmod()

# NOTE: Doctest views 'foo' and "foo" as different values (possibly because it
# compares values by looking at their `repr'). If you get a failed test like
#     Expected "foo"
#     But got  'foo'
# then just change the quote style in the test.
