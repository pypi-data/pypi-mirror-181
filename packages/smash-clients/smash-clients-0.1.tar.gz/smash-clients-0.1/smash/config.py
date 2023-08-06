# vi: set softtabstop=2 ts=2 sw=2 expandtab:
# pylint:
#
"""
Smash configuration.
"""
import os.path
import argparse
import mergeconf

# constants
APP_TAG = "Smash"
APP_NAME = "smash"
CONFIG_FILE_PATHS = [
    f"{os.path.abspath(os.path.curdir)}/{APP_NAME}.conf",
    os.path.expanduser(f"~/.config/{APP_NAME}.conf"),
    f"/etc/{APP_NAME}.conf"
]

def determine_config_file():
    """
    Determine configuration file to use.

    Returns:
        Configuration file path or None if nothing suitable found.
    """
    for path in CONFIG_FILE_PATHS:
        if os.path.exists(path):
            return path
    return None


def common():
    """ General/common client configuration.
    """
    conf = mergeconf.MergeConf(APP_TAG, files=determine_config_file())
    conf.add('server', mandatory=True)
    conf.add('request_timeout', type=int, value=30,
        description='Time limit for requests to server in seconds (default 30)')

    # get command-line options
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str,
                      help="Configuration file",
                      default=determine_config_file())
    #parser.add_argument("-d", "--debug",
    #                    help="Debug output",
    #                    action='store_true')
    #parser.add_argument("-q", "--quiet",
    #                    help="No output",
    #                    action='store_true')
    # patch in argument parser
    conf.config_argparser(parser)
    #args = parser.parse_args()

    return conf

def xbar():
    """ xbar client configuration.
    """
    conf = common()
    #xbar_conf = conf.add_section('xbar')
    #xbar_conf.add('')
    return conf
