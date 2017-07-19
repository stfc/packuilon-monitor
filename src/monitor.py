#!/usr/bin/env python2

from log_parser import BuildInfo, get_builds
from build_display import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def monitor():
    builds = get_builds('/home/htv52873/code/packuilon-monitor/test/log')
    running_builds = filter(lambda b: b.status == 'running',
                            builds)
    finished_builds = filter(lambda b: b.status != 'running',
                            builds)
    return render_template('monitor.html',
                           running_builds=running_builds,
                           finished_builds=finished_builds,
                           display_end_time=display_end_time,
                           display_build_duration=display_build_duration)

@app.route('/css/style.css')
def style():
    return render_template('templates/style.css',
        base_font_family = '"Lucida Sans Typewriter", "Lucida Console", monospace',
        icon_font_size = '20px')

if __name__ == '__main__':
    # WARNING! Debug mode means the server will accept arbitrary Python code!
    app.run('0.0.0.0', 5000 , debug = True)
