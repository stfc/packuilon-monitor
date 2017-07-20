from ansi2html import Ansi2HTMLConverter
from parse_log import get_log
from get_log import get_log_root_dir

log_converter = Ansi2HTMLConverter()

# NOTE: In the Jinja template, postfix calls to this function with the |safe
# filter, so that the HTML isn't escaped.
def display_log(logname):
    contents = get_log(logname)
    return log_converter.convert(contents, full=False)
