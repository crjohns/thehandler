import pygame
from pygame import Color
import thehandler

class Game:

    def __init__(self, window):
        self.window = window
        config = thehandler.get_config()
        self.winx = config['window_x']
        self.winy = config['window_y']

        self.scene = None


    def render(self):
        self.window.fill(Color('black'))

        if(self.scene):
            self.scene.draw(self.window)

        pygame.display.flip()
        
