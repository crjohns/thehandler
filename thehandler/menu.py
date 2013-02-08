from __future__ import print_function
import thehandler, thehandler.model
from window import *
from scene import Scene
import pygame
import random

class StartMenu(BaseWindow):

    def __init__(self):
        super(StartMenu,self).__init__()

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
                ["A - Your Name:", "B - Agency Name:", "C - Agency Abbreviation:", "D - Difficulty:"]
        newgamescene.addWindow(TextWindow(location = (0, 5), lines = lines, updown=None))

        self.name = EditText(length = 32, activateButton = pygame.K_a, \
                location = (len(lines[0]) + 1, 5), fgcolor='white')

        gender = random.sample(['male', 'female'], 1)[0]
        tempname = thehandler.model.getName(gender)

        self.name.text = tempname[0] + " " + tempname[1]

        self.agencyname = EditText(length = 32, activateButton = pygame.K_b, \
                location = (len(lines[1]) + 1, 6), fgcolor='white')
        self.agencyname.text = 'Central Terrorist Task Force'

        self.agencyabbrev = EditText(length = 8, activateButton = pygame.K_c, \
                location = (len(lines[2]) + 1, 7), fgcolor='white')

        self.agencyabbrev.text = 'CTTF'

        self.difficultyOptions = ['Easy   ($1B starting)', \
                                  'Normal ($100M starting)', \
                                  'Hard   ($10M starting)']

        self.difficulty = None

        def updateDifficulty(self, selected):
            self.selectedDifficulty = selected

            if not self.difficulty:
                self.difficulty = TextWindow(location=(len(lines[3])+1, 8), fgcolor='white', \
                        lines=[self.difficultyOptions[self.selectedDifficulty]], updown=None)
            else:
                self.difficulty.lines = [self.difficultyOptions[self.selectedDifficulty]]

            self.difficulty.clearActions()
            self.difficulty.addAction(pygame.K_d, lambda x: \
                    newgamescene.addWindow(createSelector(newgamescene, \
                                                      self.difficultyOptions, \
                                                      lambda choice: updateDifficulty(self, choice), \
                                                      border=True, \
                                                      title="Select Difficulty",\
                                                      default = selected)))

        updateDifficulty(self, 1)

        newgamescene.addWindow(self.name)
        newgamescene.addWindow(self.agencyname)
        newgamescene.addWindow(self.agencyabbrev)
        newgamescene.addWindow(self.difficulty)

        thehandler.g_game.pushScene(newgamescene)


    def draw(self, gamewindow):
        gamewindow.centerchars("Main Menu", y=0)

        loc = 5
        for option in ['A - New Game']:
            gamewindow.putchars(option, x=0, y=loc)
            loc += 1


