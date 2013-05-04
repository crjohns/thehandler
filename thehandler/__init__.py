import pygame
from pygame.locals import *
import argparse
import json
import sys
import os.path
from os.path import expanduser
from game import Game

PROGRAM_NAME = "The Handler"
VERSION = "0.0 dev"


_config_search_dirs = [expanduser('~')]

_global_config = None
_global_game = None

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
    except ValueError, e:
        print "FATAL: Parse error in configuration file %s\n%s" % (filename, e)
        sys.exit(1)

    if 'data_dir' not in _global_config:
        print "FATAL: Missing 'data_dir' setting in config file"

    (head, _) = os.path.split(filename)
    _global_config['data_dir'] = os.path.normpath(os.path.join(head, _global_config['data_dir']))

    print _global_config

    return _global_config





def get_game():
    global _global_game

    if _global_game:
        return _global_game

    config = get_config()

    window = pygame.display.set_mode((config['window_x'], config['window_y']), DOUBLEBUF | HWACCEL)
    pygame.display.set_caption(PROGRAM_NAME + " " + VERSION)
    pygame.key.set_repeat(300, 25)

    _global_game = Game(window)
    return _global_game
