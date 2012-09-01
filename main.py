import pygcurse
from scene import Scene
from window import BaseWindow
from game import Game
import pygame

PROGRAM_NAME = "The Handler"
VERSION = "0.0 dev"

winx = 80
winy = 30

gamewindow = pygcurse.PygcurseWindow(winx, winy, PROGRAM_NAME + " " + VERSION, fullscreen=False)
gamewindow.autoupdate = False



class StartMenu(BaseWindow):
    def __init__(self):
        pass

    def getActions(self):
        return [(pygame.K_a, lambda x: self.startGame())]

    def startGame(self):
        global g_game

        newgamescene = Scene()
        class NewGameWindow(BaseWindow):

            def getActions(self):
                return [(pygame.K_q, lambda x: g_game.popScene())]

            def draw(self, gamewindow):
                gamewindow.putchars("Create a new game")

        newgamescene.addWindow(NewGameWindow())

        g_game.pushScene(newgamescene)


    def printcentered(self, gamewindow, message, y):
        global winx
        gamewindow.putchars(message, x = (winx/2 - len(message)/2), y = y)

    def draw(self, gamewindow):
        gamewindow.centerchars("Main Menu", y=0)

        loc = 5
        for option in ['A - New Game']:
            gamewindow.putchars(option, x=0, y=loc)
            loc += 1


g_game = Game()

mainscene = Scene()
menu = StartMenu()
mainscene.addWindow(menu)

g_game.pushScene(mainscene)


clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            exit(0)

        if event.type == pygame.KEYDOWN:
            g_game.inchar(key = event.key, char = event.unicode)

    g_game.display(gamewindow)
    gamewindow.update()

    clock.tick(60)
