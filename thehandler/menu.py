import thehandler
from window import BaseWindow, TextWindow
from scene import Scene
import pygame

class StartMenu(BaseWindow):


    def __init__(self):
        pass

    def getActions(self):
        return [(pygame.K_a, lambda x: self.startGame())]

    def startGame(self):

        newgamescene = Scene()
        class NewGameWindow(BaseWindow):

            def getActions(self):
                return [(pygame.K_q, lambda x: thehandler.g_game.popScene())]

            def draw(self, gamewindow):
                gamewindow.putchars("Create a new game")

        newgamescene.addWindow(NewGameWindow())

        newgamescene.addWindow(TextWindow((50,0), (thehandler.WINX-50,thehandler.WINY), lines="Hello you\nThis is too long\nHow\nAre\nYou?\nMore\nMore2\nMore23\nMore4"))

        thehandler.g_game.pushScene(newgamescene)


    def draw(self, gamewindow):
        gamewindow.centerchars("Main Menu", y=0)

        loc = 5
        for option in ['A - New Game']:
            gamewindow.putchars(option, x=0, y=loc)
            loc += 1


