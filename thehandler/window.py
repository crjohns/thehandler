import thehandler
import pygame
import pygcurse

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

    def __init__(self, location=(0,0), dims=(thehandler.WINX, thehandler.WINY), title=None, lines=None, updown=(pygame.K_UP, pygame.K_DOWN), leftright=None, fgcolor=pygcurse.DEFAULTFGCOLOR):
        self.updown = updown
        self.setLines(lines)
        self.title = title
        self.topline = 0
        self.fgcolor = fgcolor
        self.location = location
        self.dims = dims
        self.leftside = 0
        self.leftright = leftright


    def setLines(self, lines):
        if lines is None:
            return
        if isinstance(lines, str):
            self.lines = lines.split('\n')
        elif isinstance(lines, list):
            self.lines = []
            for line in lines:
                self.lines += line.split('\n')
        else:
            raise TypeError("Lines are not string or list")

    def uppress(self):
        self.topline = max(self.topline-1, 0)

    def downpress(self):
        self.topline = max(min(self.topline+1, len(self.lines) - self.dims[1]), 0)

    def leftpress(self):
        self.leftside = max(0, self.leftside - 1)

    def rightpress(self):
        maxline = max(map(len, self.lines))
        self.leftside = min(self.leftside + 1, maxline-self.dims[1])


    def getActions(self):
        ret = []
        if self.updown:
            ret += [(self.updown[0], lambda x: self.uppress()),
                    (self.updown[1], lambda x: self.downpress())]
        if self.leftright:
            ret += [(self.leftright[0], lambda x: self.leftpress()),
                    (self.leftright[1], lambda x: self.rightpress())]

        return ret


    def draw(self, gamewindow):
        if self.lines:
            for (offset, line) in enumerate(self.lines[self.topline : self.topline+self.dims[1]]):
                gamewindow.putchars( \
                        line[self.leftside:self.leftside+min(len(line),self.dims[0])], \
                             x=self.location[0], y=self.location[1]+offset, \
                             fgcolor = self.fgcolor)

class EditText(BaseWindow):

    activateButton = None
    text = ""
    position = 0

    active = False

    def __init__(self, length, activateButton = None, hint = "", location = (0,0), fgcolor = \
            pygcurse.DEFAULTFGCOLOR):
        self.length = length
        self.activateButton = activateButton
        self.hint = hint
        self.location = location
        self.fgcolor = fgcolor

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
        self.active = True
        self.setPosition(len(self.text))
        self.getActions = self.__make_deactivate_actions__()
    
    def deactivate(self):
        self.active = False
        self.getActions = self.__make_activate_actions__()


    def __make_activate_actions__(self):
        if self.activateButton:
            return lambda: [(self.activateButton, lambda x: self.activate())]
        else:
            return []

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
            gamewindow.putchars(self.text, x = self.location[0], y = self.location[1], fgcolor=self.fgcolor)

        gamewindow.settint(0,0,0, (self.location[0], self.location[1], self.length, 1))
        if self.active and self.position < self.length:
            gamewindow.lighten(80, (self.location[0] + self.position, self.location[1], 1, 1))


class SelectText(BaseWindow):
    pass
