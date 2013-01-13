import pygcurse
import pygame

PROGRAM_NAME = "The Handler"
VERSION = "0.0 dev"

WINX = 80
WINY = 30

g_game = None


from thehandler.game import Game

def createGame():
    global g_game


    gamewindow = pygcurse.PygcurseWindow(WINX, WINY, PROGRAM_NAME + " " + VERSION, fullscreen=False)
    gamewindow.autoupdate = False
    
    pygame.key.set_repeat(300, 25)

    g_game = Game()

    return gamewindow

