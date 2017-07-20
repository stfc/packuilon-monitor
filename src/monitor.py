#!/usr/bin/env python2


from get_log import get_log_root_dir
from parse_log import BuildInfo, get_builds
from display_build import *
from display_log import display_log
from flask import Flask, render_template
from ansi2html import Ansi2HTMLConverter
import sys


# FIXME: This can't be right ... on the other hand, it does actually work.
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)


@app.route('/')
def monitor():
    builds = get_builds(get_log_root_dir())
    running_builds = filter(lambda b: b.status == 'running', builds)
    finished_builds = filter(lambda b: b.status != 'running', builds)
    return render_template(
        'monitor.html',
        running_builds=sort_running_builds(running_builds),
        finished_builds=sort_finished_builds(finished_builds),
        display_start_time=display_start_time,
        display_build_duration=display_build_duration)


@app.route('/log/<logname>')
def log(logname):
    return render_template('log.html',
                           body=display_log(logname),
                           name=logname)


@app.route('/css/monitor.css')
def monitor_style():
    return render_template(
        'monitor.css',
        base_font_family=(
            '"Lucida Sans Typewriter",'
            '"Lucida Console",'
            'monospace'),
        icon_font_size='20px')


@app.route('/css/log.css')
def log_style():
    return render_template(
        'log.css',
        base_font_family=(
            '"Lucida Sans Typewriter",'
            '"Lucida Console"'
            'monospace'))


if __name__ == '__main__':
    # WARNING! Debug mode means the server will accept arbitrary Python code!
    app.run('0.0.0.0', 5000, debug=True)
