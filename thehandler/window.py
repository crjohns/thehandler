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
        if lines is None:
            return
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

class EditText(BaseWindow):

    activateButton = None
    text = ""
    position = 0

    active = False

    def __init__(self, length, activateButton, hint = "", location = (0,0)):
        self.length = length
        self.activateButton = activateButton
        self.hint = hint
        self.location = location

        self.getActions = self.__make_activate_actions__()

    def activate(self):
        print "Active now"
        self.active = True
        self.position = min(len(self.text), self.length)
        self.getActions = self.__make_deactivate_actions__()
    
    def deactivate(self):
        print "Not active now"
        self.active = False
        self.getActions = self.__make_activate_actions__()


    def __make_activate_actions__(self):
        return lambda: [(self.activateButton, lambda x: self.activate())]

    def __make_deactivate_actions__(self):
        actions = [(pygame.K_RETURN, lambda x: self.deactivate())]

        for key in range(pygame.K_0, pygame.K_DELETE):
            actions.append((key, lambda x: self.doWrite(x)))

        actions.append((pygame.K_BACKSPACE, lambda x: self.backspace()))
        actions.append((pygame.K_DELETE, lambda x: self.delete()))

        return lambda: actions


    def doWrite(self, letter):
        if self.position > self.length or len(text) >= self.length:
            return
        self.text = self.text[:self.position] + letter + self.text[self.position:]
        self.position = min(self.position+1, self.length)

    def delete(self):
        self.text = self.text[:self.position] + self.text[self.position+1:]

    def backspace(self):
        self.text = self.text[:self.position-1] + self.text[self.position:]
        self.position = max(self.position-1, 0)

    def draw(self, gamewindow):
        gamewindow.putchars(self.text, x = self.location[0], y = self.location[1])
        if self.active:
            gamewindow.cursor = (self.location[0] + self.position, self.location[1])



