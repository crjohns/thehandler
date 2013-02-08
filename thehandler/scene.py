from window import BaseWindow
import pygame
import pygame.key

class Scene:
    def __init__(self):
        self.windows = []
        self.windowcmp = lambda x,y: x[0] < y[0]
        self.actions = dict()

    def addWindow(self, window, zindex=0):

        if not isinstance(window, BaseWindow):
            raise ValueError("BUG: Window is not correct type")

        self.windows.insert(0, (zindex, window))
        self.windows = sorted(self.windows, key = lambda x: x[0])

        if window.isModal():
            self.actions = dict()

        self.addActions(window.built_in_actions)
        self.addActions(window.getActions())

    def removeWindow(self, window):
        self.windows = filter(lambda x: x[1] != window, self.windows)
        self.refreshActions()

    def addActions(self, actions):
        for (key,action) in actions:
            if key in self.actions:
                raise ValueError("Action for '%s' already exists" % pygame.key.name(key))
            self.actions[key] = action

    def refreshActions(self):
        self.actions = dict()
        for (zindex, window) in self.windows:
            if window.isModal():
                self.actions = dict()

            self.addActions(window.built_in_actions)
            self.addActions(window.getActions())

            if window.isModal():
                return

    def draw(self, gamewindow):
        gamewindow.fill(" ")
        for (zindex, window) in self.windows:
            window.draw(gamewindow)

    def inchar(self, key):
        if key in self.actions:
            self.actions[key](key)
        # If another handler modifies actions, get the new ones
        self.refreshActions()
