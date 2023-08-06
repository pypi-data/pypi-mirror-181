import curses
from betterTUI.Screen import Screen

class Button:
    def __init__(self, screen: Screen, x: int, y: int, label: str, color=0, *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = len(label) +1
        self.height = 3
        self.label = label
        self.parent = None
        self.color = color

        for i in range(0, self.width+1):
            self.addstr(y, x+i, "─")
            self.addstr(y+2, x+i, "─")

        self.addstr(y, x, "┌")
        self.addstr(y, x+self.width, "┐")
        self.addstr(y+1, x, "│")
        self.addstr(y+1, x+self.width, "│")
        self.addstr(y+2, x, "└")
        self.addstr(y+2, x+self.width, "┘")

        self.addstr(y+1, x+1, label)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def on(self, *args) -> int:
        if(len(args) == 0):
            args =  ["\n", "KEY_ENTER"]
            
        self.addstr(self.y+1, self.x+1, self.label, True)

        while(True):
            key_str = self.screen.getkey()

            if key_str in args:
                self.addstr(self.y+1, self.x+1, self.label)
                curses.curs_set(0)
                return key_str

            self.screen.refresh()

    def move(self, x ,y):
        for i in range(0, self.width+1):
            self.screen.addstr(self.y, self.x+i, " ")
            self.screen.addstr(self.y+2, self.x+i, " ")

        self.screen.addstr(self.y+1, self.x, " ")
        self.screen.addstr(self.y+1, self.x+self.width, " ")

        self.screen.addstr(self.y+1, self.x+1, " "*len(self.label))

        for i in range(0, self.width+1):
            self.addstr(y, x+i, "─")
            self.addstr(y+2, x+i, "─")

        self.addstr(y, x, "┌")
        self.addstr(y, x+self.width, "┐")
        self.addstr(y+1, x, "│")
        self.addstr(y+1, x+self.width, "│")
        self.addstr(y+2, x, "└")
        self.addstr(y+2, x+self.width, "┘")

        self.addstr(y+1, x+1, self.label)

        self.x = x
        self.y = y

    def delete(self):
        for i in range(0, self.width+1):
            self.screen.addstr(self.y, self.x+i, " ")
            self.screen.addstr(self.y+2, self.x+i, " ")

        self.screen.addstr(self.y+1, self.x, " ")
        self.screen.addstr(self.y+1, self.x+self.width, " ")

        self.screen.addstr(self.y+1, self.x+1, " "*len(self.label))

        del self