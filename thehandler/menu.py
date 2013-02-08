import thehandler, thehandler.model
from window import BaseWindow, TextWindow, EditText, SelectText
from scene import Scene
import pygame
import random

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
                gamewindow.centerchars("Create a new game", y=0)

        newgamescene.addWindow(NewGameWindow())

        lines = \
                ["A - Your Name:", "B - Agency Name:", "C - Agency Abbreviation:"]
        newgamescene.addWindow(TextWindow(location = (0, 5), lines = lines, updown=None))

        name = EditText(length = 32, activateButton = pygame.K_a, \
                location = (len(lines[0]) + 1, 5), fgcolor='white')

        gender = random.sample(['male', 'female'], 1)[0]
        tempname = thehandler.model.getName(gender)

        name.text = tempname[0] + " " + tempname[1]

        agencyname = EditText(length = 32, activateButton = pygame.K_b, \
                location = (len(lines[1]) + 1, 6), fgcolor='white')
        agencyname.text = 'Central Terrorist Task Force'

        agencyabbrev = EditText(length = 8, activateButton = pygame.K_c, \
                location = (len(lines[2]) + 1, 7), fgcolor='white')

        agencyabbrev.text = 'CTTF'

        newgamescene.addWindow(name)
        newgamescene.addWindow(agencyname)
        newgamescene.addWindow(agencyabbrev)

        newgamescene.addWindow(SelectText(location = (1,20), dims=(15,2), leftright=(pygame.K_LEFT, pygame.K_RIGHT), lines=["Option A", "Option B", "Option C", "Oprtion D", "OOO E"], border=True))

        thehandler.g_game.pushScene(newgamescene)


    def draw(self, gamewindow):
        gamewindow.centerchars("Main Menu", y=0)

        loc = 5
        for option in ['A - New Game']:
            gamewindow.putchars(option, x=0, y=loc)
            loc += 1


