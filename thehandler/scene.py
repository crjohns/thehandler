from window import BaseWindow

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

        self.addActions(window.getActions())


    def addActions(self, actions):
        for (key,action) in actions:
            if key in self.actions:
                raise ValueError("Action for %s already exists" % key)
            self.actions[key] = action

    def refreshActions(self):
        for window in self.windows:
            self.addActions(window.getActions())

    def draw(self, gamewindow):
        gamewindow.fill(" ")
        for (zindex, window) in self.windows:
            window.draw(gamewindow)

    def inchar(self, key):
        if key in self.actions:
            self.actions[key](key)


