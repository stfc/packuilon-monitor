#!/usr/bin/env python2

from log_parser import BuildInfo, get_builds, get_log
from build_display import *
from flask import Flask, render_template
from ansi2html import Ansi2HTMLConverter
import sys

# FIXME: This can't be right ... on the other hand, it does actually work.
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

# FIXME: should parse Packuilon global config for this path.
# (Present also in log_display.py.)
LOGROOT = '/home/htv52873/code/packuilon-monitor/test/log'

@app.route('/')
def monitor():
    builds = get_builds(LOGROOT)
    running_builds = filter(lambda b: b.status == 'running',
                            builds)
    finished_builds = filter(lambda b: b.status != 'running',
                            builds)
    return render_template('monitor.html',
                           running_builds=running_builds,
                           finished_builds=sort_finished_builds(finished_builds),
                           display_start_time=display_start_time,
                           display_build_duration=display_build_duration)

@app.route('/log/<logname>')
def log(logname):
    conv = Ansi2HTMLConverter()
    return conv.convert(get_log(LOGROOT, logname))

@app.route('/css/style.css')
def style():
    return render_template('style.css',
        base_font_family = '"Lucida Sans Typewriter", "Lucida Console", monospace',
        icon_font_size = '20px')

if __name__ == '__main__':
    # WARNING! Debug mode means the server will accept arbitrary Python code!
    app.run('0.0.0.0', 5000 , debug = True)
