import thehandler
import bisect 
import resources
import pygame
from pygame.locals import *


def on_click_listener(view, fn):
    view.on_click = fn
    return fn

class View(object):

    """
        Generic view that supports drawing and input

        >>> view = View(0,0,1,1,100)
        >>> view2 = View(0,0,1,1,101)
        >>> view3 = View(0,0,1,1,100)
        >>> view4 = View(0,0,1,1,104)
        >>> view.addView(view2)
        >>> view.addView(view3)
        >>> view.addView(view4)
        >>> view._viewkeys
        [100, 101, 104]
        >>> view2.parent == view
        True
        >>> view.removeView(view3)
        >>> view3.parent == None
        True
        >>> view._viewkeys
        [101, 104]
        >>> view2.setZ(105)
        >>> view._viewkeys
        [104, 105]

        >>> containview = View(10,10,100,100)
        >>> containview.contains((11,11))
        True
        >>> containview.contains((101,10))
        False
        >>> subview = View(10, 10, 10, 10)
        >>> containview.addView(subview)
        >>> subview.contains((21,21))
        True
        >>> subview.contains((11,11))
        False
        >>> subsub = View(5,5,5,5)
        >>> subview.addView(subsub)
        >>> subsub.contains((26,26))
        True
        >>> subsub.contains((15,15))
        False
        >>> subsub.globalcoords((5,5))
        (25, 25)
        
        >>> containview.center_x(10)
        55
        >>> containview.center_y(60)
        30
    """


    def __init__(self, x, y, width, height, zindex = 100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.zindex = zindex
        self._viewkeys = []
        self.subviews = []
        self.parent = None

        self._click_handlers = []
        self._key_handlers = []

    def addView(self, view):
        i = bisect.bisect_left(self._viewkeys, view.zindex)
        self._viewkeys.insert(i, view.zindex)
        self.subviews.insert(i, view)
        view.parent = self

    def removeView(self, view):
        for i in range(len(self.subviews)):
            if self.subviews[i] == view:
                del self._viewkeys[i]
                del self.subviews[i]
                view.parent = None
                return
        raise ValueError("Trying to remove view that is not contained in this view")


    def setZ(self, zindex):
        self.zindex = zindex
        oldparent = self.parent
        oldparent.removeView(self)
        oldparent.addView(self)

    def draw(self, screen): 
        for view in self.subviews:
            view.draw(screen)

    # Convert global coordinates to parent-relative coordinates for this view
    def relcoords(self, pos):
        offx = 0
        offy = 0
        cur = self.parent
        while cur:
            offx += cur.x
            offy += cur.y
            cur = cur.parent

        return (pos[0] - offx, pos[1] - offy)

    # Convert parent-relative coordinates for this view to global coordinates
    def globalcoords(self, pos):
        offx = 0
        offy = 0
        cur = self.parent
        while cur:
            offx += cur.x
            offy += cur.y
            cur = cur.parent
        
        return (pos[0] + offx, pos[1] + offy)

    def on_click(self, pos, button):
        for handler in self._click_handlers:
            if handler(self, pos, button):
                return True

        for view in self.subviews:
            if view.contains(pos) and view.on_click(pos, button):
                return True
        return False

    def click_handler(self, handler):
        self._click_handlers.append(handler)

    def button_handler(self, handler, checkbutton):
        def handler2(self, pos, button):
            if button != checkbutton:
                return False
            else:
                return handler(self, pos)
        return handler2
    
    def left_click_handler(self, handler):
        self._click_handlers.append(self.button_handler(handler, 1))
    def right_click_handler(self, handler):
        self._click_handlers.append(self.button_handler(handler, 3))
    def scroll_up_handler(self, handler):
        self._click_handlers.append(self.button_handler(handler, 4))
    def scroll_down_handler(self, handler):
        self._click_handlers.append(self.button_handler(handler, 5))

    def on_hover(self, pos, isDown):
        for view in self.subviews:
            if view.contains(pos) and view.on_hover(pos, isDown):
                return True
        return False

    def on_key_event(self, key, value, isUp):
        for view in self.subviews:
            if view.on_key_event(key, value, isUp):
                return True
        return False

    def contains(self, pos):
        (x,y) = self.relcoords(pos)
        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height

    def __str__(self):
        return "View(%d,%d,%d,%d,%d)" % (self.x, self.y, self.width, self.height, self.zindex)

    def center_x(self, width, relative=True):
        if relative:
            (x,y) = self.globalcoords((0,0))
        else:
            (x,y) = (0,0)
        return self.width/2 - width/2 + x
    def center_y(self, height, relative=True):
        if relative:
            (x,y) = self.globalcoords((0,0))
        else:
            (x,y) = (0,0)
        return self.height/2 - height/2 + y


class MainMenuScene(View):

    def __init__(self, windowx, windowy):
        super(MainMenuScene, self).__init__(0,0,windowx, windowy)

        logoview = LogoView(0,0)
        logoview.x = self.center_x(logoview.width)
        self.addView(logoview)


        base = 200

        newgame = ButtonView("New Game", self.center_x(200), base, 200, 60)
        self.addView(newgame)
        loadgame = ButtonView("Load Game", self.center_x(200), base+80, 200, 60)
        self.addView(loadgame)
        scores = ButtonView("Scores", self.center_x(200), base+160, 200, 60)
        self.addView(scores)

        version = LabelView("Version " + thehandler.VERSION, \
                0, 584)
        version.y = windowy - version.height
        self.addView(version)


        @newgame.left_click_handler
        def fn(self, pos):
            thehandler.get_game().scene = NewGameScene(windowx, windowy)

class NewGameScene(View):
    def __init__(self, windowx, windowy):
        super(NewGameScene, self).__init__(0, 0, windowx, windowy)

        label = LabelView("Start New Game", 0, 40, fontsize = 32)
        label.x = self.center_x(label.width)
        self.addView(label)

        name = TextInputView("Chris Johnson", 100, 100, maxlength = 50)
        self.addView(name)

class LogoView(View):

    def __init__(self, x, y, z=100):
        self.image = resources.load_image('logo.png')
        super(LogoView, self).__init__(x,y,self.image.get_width(), self.image.get_height(), z)
        

    def draw(self, window):
        pos = self.globalcoords((self.x, self.y))
        window.blit(self.image, pos)

class LabelView(View):

    def __init__(self, text, x, y, z=100, fontsize = 16, color = Color(200,200,200)):
        self.fontsize = fontsize
        self.color = color

        self.setText(text)

        super(LabelView, self).__init__(x,y,self.surface.get_width(), self.surface.get_height(), z)

    def setText(self, text):
        self.text = text
        self.font = pygame.font.SysFont('helvetica', self.fontsize)
        self.surface = self.font.render(text, 1, self.color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def draw(self, window):
        pos = self.globalcoords((self.x, self.y))
        window.blit(self.surface, pos)

class TextInputView(LabelView):

    def __init__(self, text, x, y, z=100, fontsize=16, color = Color(200,200,200), maxlength = None):
        self.input_active = False
        super(TextInputView, self).__init__(text, x, y, z, fontsize, color)

        self.maxlength = maxlength
        self.char_offset = 0
        self.line_offset = 0
        self.text = text

        self.left_click_handler(lambda self,pos: self.left_click(pos))

    def draw(self, window):
        super(TextInputView, self).draw(window)
        if self.input_active:
            (myx, myy) = self.globalcoords((self.x, self.y))
            myx += self.line_offset
            
            pygame.draw.line(window, self.color, (myx, myy), (myx, myy+self.height))


    def setText(self, text):
        super(TextInputView, self).setText(text)
        self.width = int(self.width + 50)
        if self.input_active:
            (self.char_offset, self.line_offset) = self._find_char_offsets(min(self.char_offset, len(self.text)))

    def text_input(self, key, val):

        if key == pygame.K_RETURN:
            self.input_active = False
            thehandler.get_game().set_text_input(None)
        elif key == pygame.K_LEFT:
            (self.char_offset, self.line_offset) = self._find_char_offsets(max(self.char_offset-1,0))
        elif key == pygame.K_RIGHT:
            (self.char_offset, self.line_offset) = self._find_char_offsets(min(self.char_offset+1,len(self.text)))
        elif key == pygame.K_BACKSPACE:
            if self.char_offset > 0:
                self.char_offset -= 1
                self.setText(self.text[0:self.char_offset]+self.text[self.char_offset+1:])
        else:
            if self.char_offset < self.maxlength:
                self.char_offset += 1
                self.setText(self.text[0:self.char_offset-1] + val + self.text[self.char_offset-1:])
        return True

    def _find_pos_offsets(self, pos):
        coords = self.relcoords(pos)
        xrel = coords[0]-self.x
        asum = 0
        count = 0
        for (_,_,_,_,asc) in self.font.metrics(self.text):
            if asum+asc > xrel:
                break

            asum += asc
            count += 1

        return (count, asum)

    def _find_char_offsets(self, count):
        left = count
        asum = 0
        for (_,_,_,_,asc) in self.font.metrics(self.text):
            if left <= 0:
                break

            left -= 1
            asum += asc

        return (count, asum)

    def left_click(self, pos):
        (self.char_offset, self.line_offset) = self._find_pos_offsets(pos) 
        self.input_active = True
        thehandler.get_game().set_text_input(lambda key, val: self.text_input(key,val))



class ButtonView(View):

    def __init__(self, text, x, y, w, h, z=100, fontsize = 32):
        super(ButtonView, self).__init__(x,y,w,h,z)

        self.button_reg = pygame.Surface((w,h), HWSURFACE | SRCALPHA)
        self.button_over = pygame.Surface((w,h), HWSURFACE | SRCALPHA)
        self.button_down = pygame.Surface((w,h), HWSURFACE | SRCALPHA)
        self.button_reg.fill(Color(100,0,0))
        self.button_over.fill(Color(110,10,10))
        self.button_down.fill(Color(120,40,40))


        myfont = pygame.font.SysFont('helvetica', fontsize+0)
        surf = myfont.render(text, 1, Color(200,200,200))

        cx = self.center_x(surf.get_width(), False)
        cy = self.center_y(surf.get_height(), False)
        self.button_reg.blit(surf, (cx, cy))
        self.button_down.blit(surf, (cx, cy))
        self.button_over.blit(surf, (cx, cy))

        self.curbutton = self.button_reg

    def on_hover(self, pos, isDown):
        if not isDown:
            self.curbutton = self.button_over
        else:
            self.curbutton = self.button_down


    def draw(self, window):
        pos = self.globalcoords((self.x, self.y))
        window.blit(self.curbutton, pos)
        self.curbutton = self.button_reg #reset to clear hover effects

if __name__ == "__main__":
    import doctest
    doctest.testmod()




