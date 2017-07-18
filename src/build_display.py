from logparser import *
import datetime
import humanize

def display_end_time(b):
    return humanize.naturaltime(datetime.date.fromtimestamp(b.end_time))

def display_build_duration(b):
    return humanize.naturaldelta(b.end_time - b.start_time)
