import thehandler
import pygame

class BaseWindow:
    def __init__(self):
        pass

    def getActions(self):
        return []

    def draw(self, gamewindow):
        pass


class TextWindow(BaseWindow):

    def __init__(self, location=(0,0), dims=(thehandler.WINX, thehandler.WINY), title=None, lines=None, updown=(pygame.K_UP, pygame.K_DOWN)):
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


