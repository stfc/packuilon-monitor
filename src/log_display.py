from ansi2html import Ansi2HTMLConverter

# FIXME: should parse Packuilon global config for this path.
# (Present also in monitory.py.)
LOGROOT = '/home/htv52873/code/packuilon-monitor/test/log'

log_converter = Ansi2HTMLConverter(inline = True)

# NOTE: In the Jinja template, postfix calls to this function with the |safe
# filter, so that the HTML isn't escaped.
def display_log(logname):
    contents = get_log(LOGROOT, logname)
    return log_converter(contents)
