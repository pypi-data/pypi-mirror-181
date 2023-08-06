import curses
from betterTUI.Screen import Screen

class Input:
    def __init__(self, screen: Screen, x: int, y: int, width: int, label: str, color=0, content="", *args):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = 4
        self.label = label
        self.content = content
        self.show_content = ""
        self.show_content_pos = 0
        self.pos = 0
        self.parent = None
        self.color = color

        for i in range(0, width+1):
            self.addstr(y+1, x+i, "─")
            self.addstr(y+3, x+i, "─")

        self.addstr(y+1, x, "┌")
        self.addstr(y+1, x+width, "┐")
        self.addstr(y+2, x, "│")
        self.addstr(y+2, x+width, "│")
        self.addstr(y+3, x, "└")
        self.addstr(y+3, x+width, "┘")

        self.addstr(y, x, label)

        if(len(content) < self.width-3):
            self.show_content = self.content
            self.show_content_pos = len(self.content)
        else:
            self.show_content = self.content[0:self.width-3]
            self.show_content_pos = self.width-3

        self.addstr(y+2, x+2, self.show_content)

    def addstr(self, y:int, x:int, content:str, reverse=False):
        i = 0
        if (reverse): i = 1

        self.screen.attron(curses.color_pair(self.color+i))
        self.screen.addstr(y, x, content)
        self.screen.attroff(curses.color_pair(self.color+i))

    def on(self, *args) -> int:
        if(len(args) == 0):
            args = ["\n", "KEY_ENTER"]

        self.addstr(self.y, self.x, self.label, True)
        self.screen.move(self.y+2, self.x+2+self.pos)
        curses.curs_set(1)
        self.show_content_pos = len(self.content)-1

        while(True):
            key_str = self.screen.getkey()
            if key_str in args: 
                if not(key_str == "KEY_RIGHT" or key_str == "KEY_LEFT"):
                    self.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "KEY_RIGHT") and (self.pos == len(self.show_content)) and (self.show_content_pos >= len(self.content) - 1)):
                    self.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                elif((key_str == "KEY_LEFT") and (self.pos == 0) and ((self.show_content_pos - len(self.show_content)) <= 0)):
                    self.addstr(self.y, self.x, self.label)
                    curses.curs_set(0)
                    return key_str
                else:
                    self.handle_key(key_str)
            else:
                self.handle_key(key_str)

            self.addstr(self.y+2, self.x+2, " "*(self.width-2))
            self.addstr(self.y+2, self.x+2, self.show_content)
            self.screen.move(self.y+2, self.x+2+self.pos)
            self.screen.refresh()

    def handle_key(self, key_str):
        pos = self.pos

        len_content = len(self.content)
        len_show_content = len(self.show_content)
        combined_pos = (self.show_content_pos - len_show_content) + 1 + pos
        input_length = self.width-3

        if(key_str in ["\b", "KEY_BACKSPACE"]):
            # if smaller & at end
            if(len_show_content == len_content and pos == len_show_content):
                self.content = self.content[:-1]

                if not(pos == 0):
                    self.pos -= 1
                else:
                    self.show_content_pos -= 1

            # if smaller & in middle or beginning
            elif(len_show_content == len_content and pos < len_show_content and self.show_content_pos > 0):                    
                self.content = self.content[:pos-1] + self.content[-(len(self.content)-pos):]
                self.pos -= 1

            # if bigger & at end
            elif(not len_show_content == len_content and pos == len_show_content):
                self.content = self.content[:self.show_content_pos] + self.content[self.show_content_pos+1:]
                self.show_content_pos -= 1

            # if bigger & in middle or beginning
            elif(not len_show_content == len_content and pos < len_show_content and combined_pos > 0):
                self.content = self.content[:combined_pos-1] +  self.content[-(len(self.content)-combined_pos):]
                
                if not (self.show_content_pos - len_show_content <= 0):
                    self.show_content_pos -= 1
                elif (pos > 0):
                    self.pos -= 1

        elif(key_str == "KEY_RIGHT"):
            # TRAVEL INPUT TO RIGHT
            if (pos < len_show_content):
                self.pos += 1
            elif(pos == len_show_content and not (self.show_content_pos >= len_content-1)):
                self.show_content_pos += 1
                self.show_content = self.show_content[1:] + self.content[self.show_content_pos]

        elif(key_str == "KEY_LEFT"):
            # TRAVEL INPUT TO LEFT
            if not (pos == 0):
                self.pos -= 1
            elif(pos == 0 and ((self.show_content_pos - len_show_content) >= 0)):
                if(len_show_content > 0):
                    self.show_content = self.content[self.show_content_pos - len_show_content] + self.show_content[:-1]
                    self.show_content_pos -= 1

        elif(len(key_str) == 1):
            if(key_str.isprintable()):

                # if smaller & at end
                if(len_show_content == len_content and pos == len_show_content):
                    self.content += key_str

                    if not(pos == input_length):
                        self.pos += 1
                    else:
                        self.show_content_pos += 1

                # if smaller & in middle or beginning
                elif(len_show_content == len_content and pos < len_show_content):                    
                    self.content = self.content[:pos] + key_str + self.content[-(len(self.content)-pos):]
                    self.pos += 1

                # if bigger & at end
                elif(not len_show_content == len_content and pos == len_show_content):
                    self.show_content_pos += 1
                    self.content = self.content[:self.show_content_pos] + key_str + self.content[self.show_content_pos:]

                # if bigger & in middle or beginning
                elif(not len_show_content == len_content and pos < len_show_content):
                    self.content = self.content[:combined_pos] + key_str + self.content[-(len(self.content)-combined_pos):]
                    self.pos += 1
        
        if(len_content < input_length):
            self.show_content = self.content
            self.show_content_pos = pos
        else:
            self.show_content = self.content[(self.show_content_pos-len_show_content)+1:self.show_content_pos+1]

    def move(self, x ,y):

        for i in range(0, self.width+1):
            self.screen.addstr(self.y+1, self.x+i, " ")
            self.screen.addstr(self.y+3, self.x+i, " ")

        self.screen.addstr(self.y+2, self.x, " ")
        self.screen.addstr(self.y+2, self.x+self.width, " ")

        self.screen.addstr(self.y+2, self.x+2, " "*(self.width-2))
        self.screen.addstr(self.y, self.x, " "*len(self.label))

        for i in range(0, self.width+1):
            self.addstr(y+1, x+i, "─")
            self.addstr(y+3, x+i, "─")

        self.addstr(y+1, x, "┌")
        self.addstr(y+1, x+self.width, "┐")
        self.addstr(y+2, x, "│")
        self.addstr(y+2, x+self.width, "│")
        self.addstr(y+3, x, "└")
        self.addstr(y+3, x+self.width, "┘")

        self.addstr(y, x, self.label)
        self.addstr(y+2, x+2, self.show_content)

        self.x = x
        self.y = y

    def delete(self):

        for i in range(0, self.width+1):
            self.screen.addstr(self.y+1, self.x+i, " ")
            self.screen.addstr(self.y+3, self.x+i, " ")

        self.screen.addstr(self.y+2, self.x, " ")
        self.screen.addstr(self.y+2, self.x+self.width, " ")

        self.screen.addstr(self.y+2, self.x+2, " "*(self.width-2))
        self.screen.addstr(self.y, self.x, " "*len(self.label))

        del self
