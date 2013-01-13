import thehandler
import pygame

class BaseWindow:
    def __init__(self):
        pass

    def getActions(self):
        return []

    def draw(self, gamewindow):
        pass

    # Return True if this is the only window which can have input 
    # at the current time, False otherwise
    def isModal(self):
        return False


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


    def setPosition(self, pos):
        if pos < 0:
            self.position = 0
        elif pos > self.length:
            self.position = self.length
        elif pos > len(self.text):
            self.position = len(self.text)
        else:
            self.position = pos

    def activate(self):
        print "Active now"
        self.active = True
        self.setPosition(len(self.text))
        self.getActions = self.__make_deactivate_actions__()
    
    def deactivate(self):
        print "Not active now"
        self.active = False
        self.getActions = self.__make_activate_actions__()


    def __make_activate_actions__(self):
        return lambda: [(self.activateButton, lambda x: self.activate())]

    def __make_deactivate_actions__(self):
        actions = [(pygame.K_RETURN, lambda x: self.deactivate())]

        for key in range(pygame.K_SPACE, pygame.K_DELETE):
            actions.append((key, lambda x: self.doWrite(x)))

        actions.append((pygame.K_BACKSPACE, lambda x: self.backspace()))
        actions.append((pygame.K_DELETE, lambda x: self.delete()))

        actions.append((pygame.K_LEFT, lambda x: self.setPosition(self.position - 1)))
        actions.append((pygame.K_RIGHT, lambda x: self.setPosition(self.position + 1)))

        return lambda: actions

    def isModal(self):
        return self.active


    def doWrite(self, letter):
        if self.position > self.length or len(self.text) >= self.length:
            return
        self.text = self.text[:self.position] + chr(letter) + self.text[self.position:]
        self.setPosition(self.position + 1)

    def delete(self):
        self.text = self.text[:self.position] + self.text[self.position+1:]

    def backspace(self):
        self.text = self.text[:self.position-1] + self.text[self.position:]
        self.setPosition(self.position - 1)

    def draw(self, gamewindow):
        if len(self.text) == 0 and not self.active:
            gamewindow.putchars(self.hint, x = self.location[0], y = self.location[1], fgcolor='gray')
        else:
            gamewindow.putchars(self.text, x = self.location[0], y = self.location[1])

        gamewindow.settint(0,0,0, (self.location[0], self.location[1], self.length, 1))
        if self.active and self.position < self.length:
            gamewindow.lighten(80, (self.location[0] + self.position, self.location[1], 1, 1))



