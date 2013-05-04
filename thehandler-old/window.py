import thehandler
import pygame
import pygcurse

class BaseWindow(object):

    modal = False

    def __init__(self, location=(0,0), dims=(thehandler.WINX, thehandler.WINY), modal = False):
        self.location = location
        self.dims = dims
        self.modal = modal
        self.built_in_actions = []

    def getActions(self):
        return self.built_in_actions

    def addAction(self, key, handler):
        self.built_in_actions.append((key, handler))

    def clearActions(self):
        self.built_in_actions = []

    def draw(self, gamewindow):
        pass

    # Return True if this is the only window which can have input 
    # at the current time, False otherwise
    def isModal(self):
        return self.modal


class TextWindow(BaseWindow):

    def __init__(self, location=(0,0), dims=(thehandler.WINX, thehandler.WINY), title=None, lines=None, updown=(pygame.K_UP, pygame.K_DOWN), leftright=None, fgcolor=pygcurse.DEFAULTFGCOLOR, border=False, status = None):
        super(TextWindow, self).__init__(location, dims)
        self.updown = updown
        self.setLines(lines)
        self.title = title
        self.topline = 0
        self.fgcolor = fgcolor
        self.leftside = 0
        self.leftright = leftright
        self.border = border
        self.status = status


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
        if self.border:
            gamewindow.drawline(char='+', \
                    start_pos=(self.location[0]-1, self.location[1]-1), \
                    end_pos=(self.location[0]+self.dims[0],self.location[1]-1), \
                    fgcolor=self.fgcolor)
            gamewindow.drawline(char='+', \
                    start_pos=(self.location[0]-1, self.location[1]+self.dims[1]), \
                    end_pos=(self.location[0]+self.dims[0],self.location[1]+self.dims[1]), \
                    fgcolor=self.fgcolor)
            gamewindow.drawline(char='-', \
                    start_pos=(self.location[0], self.location[1]-1), \
                    end_pos=(self.location[0]+self.dims[0]-1,self.location[1]-1), \
                    fgcolor=self.fgcolor)
            gamewindow.drawline(char='-', \
                    start_pos=(self.location[0], self.location[1]+self.dims[1]), \
                    end_pos=(self.location[0]+self.dims[0]-1,self.location[1]+self.dims[1]), \
                    fgcolor=self.fgcolor)
            gamewindow.drawline(char='|', \
                    start_pos=(self.location[0]-1, self.location[1]), \
                    end_pos=(self.location[0]-1,self.location[1]+self.dims[1]-1), \
                    fgcolor=self.fgcolor)
            gamewindow.drawline(char='|', \
                    start_pos=(self.location[0]+self.dims[0], self.location[1]), \
                    end_pos=(self.location[0]+self.dims[0],self.location[1]+self.dims[1]-1), \
                    fgcolor=self.fgcolor)
        
        if self.title:
            gamewindow.centerchars(self.title, \
                    offset=self.location[0], \
                    width=self.dims[0], \
                    y=self.location[1]-1, \
                    fgcolor=self.fgcolor)

        if self.status:
            gamewindow.putchars(self.status, \
                    x = self.location[0]+self.dims[0]-len(self.status), \
                    y = self.location[1]+self.dims[1],
                    fgcolor = self.fgcolor)

class SelectText(TextWindow):
    selected = 0
    statbar = False

    def __init__(self, location=(0,0), dims=(thehandler.WINX, thehandler.WINY), title=None, lines=None, updown=(pygame.K_UP, pygame.K_DOWN), leftright=None, fgcolor=pygcurse.DEFAULTFGCOLOR, border=False, statbar=False):
        super(SelectText, self).__init__(location, dims, title, lines, updown, leftright, fgcolor, border)
        self.statbar = statbar

    def draw(self, gamewindow):
        TextWindow.draw(self, gamewindow)

        gamewindow.lighten(80, ( \
                self.location[0], \
                self.location[1]+self.selected-self.topline,
                self.dims[0], 1))

        self.status = "%d/%d" % (self.selected+1,len(self.lines))


    def downpress(self):
        self.selected = min(self.selected+1, len(self.lines) - 1)
        if self.selected > (self.dims[1] - self.topline - 1):
            TextWindow.downpress(self)

    def uppress(self):
        self.selected = max(self.selected-1, 0)
        if self.selected < self.topline:
            TextWindow.uppress(self)
        

class EditText(BaseWindow):

    activateButton = None
    text = ""
    position = 0

    active = False

    def __init__(self, length, activateButton = None, hint = "", location = (0,0), fgcolor = \
            pygcurse.DEFAULTFGCOLOR):
        super(EditText, self).__init__(location, (length, 1))
        self.activateButton = activateButton
        self.hint = hint
        self.fgcolor = fgcolor

        self.getActions = self.__make_activate_actions__()


    def setPosition(self, pos):
        if pos < 0:
            self.position = 0
        elif pos > self.dims[0]:
            self.position = self.dims[0]
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
        if self.position > self.dims[0] or len(self.text) >= self.dims[0]:
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

        if self.active and self.position < self.dims[0]:
            gamewindow.lighten(80, (self.location[0] + self.position, self.location[1], 1, 1))


class ModalWrapper(BaseWindow):
    
    def __init__(self, scene, window, dismisskey=pygame.K_RETURN, dismisshandler=lambda sc,wrap: sc.removeWindow(wrap)):
        super(ModalWrapper,self).__init__( \
                location=(thehandler.WINX/2-(window.dims[0]/2), \
                          thehandler.WINY/2-(window.dims[1]/2)), \
                dims=window.dims,
                modal=True)
        window.location = self.location
        self.dismisskey = dismisskey
        self.dismisshandler = dismisshandler
        self.scene = scene
        self.window = window
        self.modal = True

    def getActions(self):
        ret = self.window.getActions()

        ret = filter(lambda x: x[0] != self.dismisskey, ret)
        ret.append((self.dismisskey, lambda x: self.dismisshandler(self.scene, self)))

        return ret

    def draw(self, gamewindow):
        gamewindow.settint(-100, -100, -100, region=(0,0,thehandler.WINX, thehandler.WINY))
        gamewindow.settint(0,0,0, region=(self.location[0], self.location[1], self.dims[0], self.dims[1]))
        gamewindow.fill('', (self.location[0], self.location[1], self.dims[0], self.dims[1]))
        self.window.draw(gamewindow)

def createAlert(scene, lines = [], title = None, fgcolor='white', border=False):
    width = max(map(len, lines))
    modal = ModalWrapper(scene, \
                TextWindow(dims=(width, min(len(lines), 20)), \
                           lines = lines, \
                           title = title, \
                           fgcolor = fgcolor, \
                           border = border, \
                           status = 'Enter: Close'))

    return modal

def createSelector(scene, choices, callback, default=0, title = None, fgcolor = 'white', border=False):

    def handle(sc, win):
        sc.removeWindow(win)
        callback(win.window.selected)

    width = max(map(len, choices))
    modal = ModalWrapper(scene, \
                SelectText(dims=(width, min(len(choices), 10)), \
                           lines=choices, \
                           statbar=True, \
                           fgcolor=fgcolor, \
                           border=border, \
                           title=title), \
                dismisshandler = handle)

    return modal
