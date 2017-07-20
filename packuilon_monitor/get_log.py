import os
from ConfigParser import RawConfigParser


PACKER_CONFIG = '/etc/packer-utils/config.ini'


def get_log_root_dir():
    configparser = RawConfigParser()
    configparser.read(PACKER_CONFIG)
    return configparser.get('rabbit2packer','LOG_DIR')


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
