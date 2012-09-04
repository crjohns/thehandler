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
        global winx,winy

        newgamescene = Scene()
        class NewGameWindow(BaseWindow):

            def getActions(self):
                return [(pygame.K_q, lambda x: g_game.popScene())]

            def draw(self, gamewindow):
                gamewindow.putchars("Create a new game")

        newgamescene.addWindow(NewGameWindow())

        newgamescene.addWindow(TextWindow((50,0), (winx-50,winy), lines="Hello you\nThis is too long\nHow\nAre\nYou?\nMore\nMore2\nMore23\nMore4"))

        g_game.pushScene(newgamescene)


    def draw(self, gamewindow):
        gamewindow.centerchars("Main Menu", y=0)

        loc = 5
        for option in ['A - New Game']:
            gamewindow.putchars(option, x=0, y=loc)
            loc += 1

class TextWindow(BaseWindow):

    def __init__(self, location=(0,0), dims=(winx, winy), title=None, lines=None, updown=(pygame.K_UP, pygame.K_DOWN)):
        self.updown = updown
        self.setLines(lines)
        self.title = title
        self.topline = 0

        self.location = location
        self.dims = dims


    def setLines(self, lines):
        if isinstance(lines, str):
            self.lines = lines.split('\n')
        elif isinstance(lines, list):
            self.lines = lines
        else:
            raise TypeError("Lines are not string or list")

    def uppress(self):
        self.topline = max(self.topline-1, 0)

    def downpress(self):
        self.topline = max(min(self.topline+1, len(self.lines) - self.dims[1]), 0)


    def getActions(self):
        return [(self.updown[0], lambda x: self.uppress()),
                (self.updown[1], lambda x: self.downpress())]

    def draw(self, gamewindow):
        if self.lines:
            for (offset, line) in enumerate(self.lines[self.topline : self.topline+self.dims[1]]):
                gamewindow.putchars(line[:self.dims[0]], x=self.location[0], y=self.location[1]+offset)



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
