# ╭╮╯╰─│
import shutil
import sys
import atexit
from colors import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def reset_cursor():
    sys.stdout.write("\033[u")

atexit.register(clear_screen)
atexit.register(reset_cursor)


class Window:
    def __init__(self):
        self.coord = [0,0]
        self.width:int = -1
        self.height:int = -1
        self.title = "Window"
        self.items = []
    
    def toDraw(self):
        text = f'╭─{self.title}'+("─" * (self.width - len(self.title) - 3))+"╮\n"
        for _ in range(self.height):
            text += '│'+(" " * (self.width-2))+"│\n"
        text += "╰─"+ ("─" * (self.width-4)) + "─╯"
        return text
    def reset_cursor(self):
        sys.stdout.write("\033[u")
        
    def plot(self, coord, text):
        self.reset_cursor()
        text = text.split("\n")
        for i in range(len(text)):
            print('\033[{};{}H{}'.format(coord[1]+i, coord[0]+1, text[i]), end='', flush=True)
        
    def init(self, coord=[0,0], w:int=-1, h:int=-1 , title="Window"):
        self.coord = coord
        self.width = w
        self.height = h
        self.title = title
    
    def draw(self):
        if self.height == -1:
            res = shutil.get_terminal_size()
            self.width, self.height = res.columns, res.lines
    
        text = self.toDraw()
        self.reset_cursor()  # Reset cursor before printing
        self.plot(self.coord, text)
        # print(self.items)
        if len(self.items) != 0:

            for i in self.items:
                try:
                    alignment = i[1][-1]
                except:
                    alignment = i[2]
                # print(alignment)
                if "list" in i[0]:
                    for index, item in enumerate(i[1][0]):
                        
                        x = int(self.coord[0]+2)
                        y = int(self.coord[1]+2+index)
                        if alignment in ["centerx", "centerxy"]:
                            x += int(self.width//2) - len(item)//2
                        if alignment in ["centery", "centerxy"]:
                            y += int(self.height//2) - len(i[1][0])//2
                        
                        if len(i) == 3:
                            item = item[1]
                            if i[2] != -1:
                                if index == i[2]:
                                    self.plot([x, y], rgbFg((255,255,255))+" "+item+clear_colors())
                                else:
                                    self.plot([x, y], rgbFg((138, 124, 110))+item+clear_colors())
                            elif len(i) == 2:
                                self.plot([x, y], rgbFg((255,255,255))+" "+item+clear_colors())
                                
                            else:
                                self.plot([x, y], rgbFg((138, 124, 110))+item+clear_colors())

                        else:
                            self.plot([x, y], rgbFg((255,255,255))+item+clear_colors())
                            
                            
                elif "text" in i[0]:
                    item = i[1]
                    x = int(self.coord[0]+2)
                    y = int(self.coord[1]+1)
                    if alignment in ["centerx", "centerxy"]:
                        x += int(self.width//2) - len(item)//2
                    if alignment in ["centery", "centerxy"]:
                        y += int(self.height//2) - len(i[1][0])//2

                    self.plot([x, y], rgbFg((255,255,255))+item+clear_colors())
                        

                    
    def changeIndex(self, name, index):
        for item in self.items:
            if item[0] == name:
                item[2] = index

    def addItem(self, name, item, alignment, selectable):
        if type(item) == list:
            if selectable:
                self.items.append([name, [item, alignment], 0])
            else:
                self.items.append([name, [item, alignment]])
        elif type(item) == str:
            self.items.append([name, item, alignment])

    def removeItem(self, name):
        for i, j in enumerate(self.items):
            if name == j[0]:
                self.items.pop(i)    

    def editItem(self, name, newValue):
        for i, item in enumerate(self.items):
            if name == item[0]:
                self.items[i][1] = newValue
    
    def editElement(self, name, index, newValue):
        for i, j in enumerate(self.items):
            if j[0] == name:
                self.items[i][1][index] = newValue

    def getItem(self, name:str):
        for i in self.items:
            if name == i[0]:
                return i
        return False
