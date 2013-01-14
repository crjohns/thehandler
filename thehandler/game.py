from scene import Scene
import thehandler

class Game:
    def __init__(self):
        # The scene stack is used to support going into and out of view modes
        self.scenestack = []
        # The share map is used to share data between parts of the application
        self.sharemap = None

    def pushScene(self, scene):
        if not isinstance(scene, Scene):
            raise ValueError("BUG: Object is not a Scene")
        self.scenestack.insert(0, scene)

    def popScene(self):
        self.scenestack = self.scenestack[1:]

    def getShare(self, key):
        if not key in self.sharemap:
            return None
        else:
            return self.sharemap[key]

    def putShare(self, key, val):
        self.sharemap[key] = val

    def delShare(self, key):
        self.sharemap.remove(key)

    # Display current scene
    def display(self, gamewindow):
        gamewindow.settint(0,0,0, (0,0, thehandler.WINX, thehandler.WINY))
        if len(self.scenestack) >= 1:
            self.scenestack[0].draw(gamewindow)

    # Hand input to current scene
    def inchar(self, key, char):
        if len(self.scenestack) >= 1:
            self.scenestack[0].inchar(key)
