import bisect 
import resources

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


    def on_click(self, pos):
        for view in self.subviews:
            if view.on_click(self, pos):
                return True
        return False

    def on_hover(self, pos):
        for view in self.subviews:
            if view.on_hover(self, pos):
                return True
        return False

    def on_key_event(self, key, value, isUp):
        for view in self.subviews:
            if view.on_key_event(self, pos):
                return True
        return False

    def contains(self, pos):
        (x,y) = self.relcoords(pos)
        return x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height

    def __str__(self):
        return "View(%d,%d,%d,%d,%d)" % (self.x, self.y, self.width, self.height, self.zindex)

    def center_x(self, width):
        return self.width/2 - width/2 + self.x
    def center_y(self, height):
        return self.height/2 - height/2 + self.y


class MainMenuScene(View):

    def __init__(self, windowx, windowy):
        super(MainMenuScene, self).__init__(0,0,windowx, windowy)

        logoview = LogoView(0,0)
        logoview.x = self.center_x(logoview.width)
        self.addView(logoview)


class LogoView(View):

    def __init__(self, x, y, z=100):
        self.image = resources.load_image('logo.png')
        super(LogoView, self).__init__(x,y,self.image.get_width(), self.image.get_height(), z)
        

    def draw(self, window):
        pos = self.globalcoords((self.x, self.y))
        window.blit(self.image, (pos[0], pos[1]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()




