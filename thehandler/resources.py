import thehandler
import pygame
import os

def load_image(filename):
    config = thehandler.get_config()

    path = os.path.join(config['data_dir'], filename)
    return pygame.image.load(path)
