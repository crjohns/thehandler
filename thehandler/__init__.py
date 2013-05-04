import pygame
import pygl2d
import argparse
import json
import sys
import os.path
from os.path import expanduser

PROGRAM_NAME = "The Handler"
VERSION = "0.0 dev"


_config_search_dirs = [expanduser('~')]

_global_config = None

def get_config():
    global _config_search_dirs
    global _global_config

    if _global_config:
        return _global_config


    parser = argparse.ArgumentParser(description = PROGRAM_NAME + " " + VERSION)
    parser.add_argument('-c', help='Configuration file to use', dest='configfile', metavar="file")
    args = parser.parse_args()

    filename = None

    if args.configfile:
        filename = args.configfile
    else:
        for name in _config_search_dirs:
            if os.path.isfile(os.path.join(name,'.thehandlerrc')):
                filename = os.path.join(name, '.thehandlerrc')
                break

    if not filename:
        print "FATAL: Configuration file not found (searched %s)" % str(_config_search_dirs)
        sys.exit(1)

    try:
        f = open(filename)
        _global_config = json.load(f)
        f.close()
    except IOError, e:
        print "FATAL: Failed to load configuration file (%s)" % str(e)
        sys.exit(1)

    return _global_config





def createGame():

    config = get_config()

    screen = pygl2d.display.set_mode((config['window_x'], config['window_y']), pygame.DOUBLEBUF)
    pygame.display.set_caption(PROGRAM_NAME + " " + VERSION)
    pygame.key.set_repeat(300, 25)

    return screen 

