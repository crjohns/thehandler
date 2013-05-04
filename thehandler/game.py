import pygame
from pygame import Color
import thehandler
import view

class Game:

    def __init__(self, window):
        self.window = window
        config = thehandler.get_config()
        self.winx = config['window_x']
        self.winy = config['window_y']

        self.scene = view.MainMenuScene(self.winx, self.winy)


    def mouse_move(self, pos, leftDown):
        if self.scene:
            self.scene.on_hover(pos, leftDown)

    def mouse_click(self, pos, button):
        if self.scene:
            self.scene.on_click(pos, button)


    def render(self):
        self.window.fill(Color('black'))

        if(self.scene):
            self.scene.draw(self.window)

        pygame.display.flip()
        
