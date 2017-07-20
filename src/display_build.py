from parse_log import BuildInfo
import datetime
import humanize


def display_start_time(b):
    t1 = b.start_time
    return humanize.naturaltime(datetime.datetime.fromtimestamp(t1))


def display_build_duration(b):
    t0 = b.start_time
    t1 = b.end_time
    if t0 and t1:
        return humanize.naturaldelta(t1 - t0)
    else:
        return '<span class="ran-for-cancelled">cancelled</span>'


def sort_finished_builds(builds):
    '''Sort a list of finished builds by start time from newest to oldest.'''
    return reversed(sorted(builds, key=lambda b: b.start_time))


def sort_running_builds(builds):
    '''Sort a list of running builds by start time from oldest to newest.'''
    return sorted(builds, key=lambda b: b.start_time)
