import curses

PROGRAM_NAME = "The Handler"
VERSION = "0.0 dev"


def newfullwin():
    ret = curses.newwin(24, 80, 0, 0)
    ret.nodelay(1)
    return ret
    


class GameLooper:

    def __init__(self):
        pass

    def event(self, window):
        char = window.getch()
        if(char == -1):
            return char
        if chr(char) == 'q' or chr(char) == 'Q':
            exit(0)
        return char

    def relax(self):
        curses.napms(20)





class Menu:

    def __init__(self, title=None, options=[], actions=[]):
        self._title = title
        self._options = options
        self._actions = actions

    def run(self, game):
        while True:
            char = game.event(self._window)
            offset = char - ord('A')
            if not offset in range(0, len(self._actions)):
                offset = char - ord('a')

            if offset in range(0, len(self._actions)):
                if not self._actions[offset]():
                    return
            
            game.relax()

    def start(self, game):
        self._window = newfullwin()
        
        if self._title:
            self._window.addstr(0, 40-len(self._title)/2, self._title)

        line = 5
        letter = ord('A')
        for option in self._options:
            self._window.addstr(line, 0, chr(letter) + ' - ' + option)
            line += 1
            letter += 1

        self._window.refresh()

        self.run(game)


def startup(screen):
    curses.curs_set(0)

    game = GameLooper()


    false = lambda: False

    menu = Menu(PROGRAM_NAME + " " + VERSION,
            ["New Game", "Load Game", "Statistics"], [false, None, None])



    menu.start(game)


curses.wrapper(startup)
