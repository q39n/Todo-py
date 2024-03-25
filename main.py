from colors import *
from readchar import readchar, key
from todo import Todo
from keys import *
import cursor
from string import punctuation, digits, ascii_letters

class Main:

    def __init__(self):
        self.todo = Todo()
        self.windows = [self.todo.progressWindow, self.todo.doneWindow]
        self.winIndex = 0
        self.itemIndex = 0
        self.running = True
        self.mode = "todo"
        self.add_todo_msg = 0
        self.todos_len = [-1,0]
    
    def wrap_indexes(self):
        self.todos_len = []
        self.todos_len.append(len(self.windows[0].getItem("list")[1][0])-1)
        self.todos_len.append(len(self.windows[1].getItem("list")[1][0])-1)
        self.to_show_empty_msg()
        
        if self.winIndex == 0:
            self.windows[1].changeIndex("list", -1)
        elif self.winIndex == 1:
            self.windows[0].changeIndex("list", -1)
        self.windows[self.winIndex].changeIndex("list", self.itemIndex)

        if self.itemIndex > self.todos_len[self.winIndex]:
            self.itemIndex = self.todos_len[self.winIndex]
        elif self.itemIndex < 0:
            self.itemIndex = 0

    def to_show_empty_msg(self):
        if self.todos_len[0]+1 == 0 and self.add_todo_msg == 0:
            self.add_todo_msg += 1
            self.windows[0].addItem("no_todos_list", ["No Todos?", "Press [A] to add one!"], "centerxy", False)
            self.todos_len[0] -= 1
        elif self.add_todo_msg == 1 and self.todos_len[0] == 0:
            self.add_todo_msg -= 1
            self.todos_len[0] -= 1
            self.windows[0].removeItem("no_todos_list")


    def handle_input(self):
        
        k = readchar()

        if k == "q" and self.mode != 'adding':
            self.todo.savetxt()
            self.running = False


        if self.mode == "todo":
            # For the Todo windows
            if k == "e" and self.todos_len[self.winIndex]+1 != 0:
                cursor.show()
                self.todo.tfData = self.todo.progress[self.itemIndex][1]
                self.mode = "editing"
                self.todo.tfWindow.editItem("text", self.todo.tfData)

            if k == "a":
                cursor.show()
                self.todo.tfData = ''
                self.mode = "adding"
            
            if self.todos_len[self.winIndex] > -1:
                if k == "d":
                    if self.winIndex == 0:
                        self.todo.progress.pop(self.itemIndex)
                    elif self.winIndex == 1:
                        self.todo.done.pop(self.itemIndex)
                    self.itemIndex -= 1 if self.itemIndex > 0 else 0
                
                
            
            #Selecting Movement
            if k in UP:
                if self.itemIndex > 0:
                    self.itemIndex -= 1
                else:
                    self.itemIndex = self.todos_len[self.winIndex]
            if k in DOWN:
                if self.itemIndex < self.todos_len[self.winIndex]:
                    self.itemIndex += 1
                else:
                    self.itemIndex = 0
            
            if k in RIGHT:
                if self.todos_len[1]+1 > 0:
                    self.winIndex = 1
                    if self.itemIndex > self.todos_len[self.winIndex]:
                        self.itemIndex = self.todos_len[self.winIndex]
                    elif self.todos_len[0] < 0:
                        self.itemIndex = 0

            if k in LEFT:
                if self.todos_len[1]+1 > 0:
                    self.winIndex = 0

                    if self.itemIndex > self.todos_len[self.winIndex]:
                        self.itemIndex = self.todos_len[self.winIndex]   
                    elif self.todos_len[0] < 0:
                        self.itemIndex = 0

            # To move Todos back and forth
            if k in key.CTRL_L and self.winIndex == 0:
                self.todo.moveTodo(self.itemIndex, 0)
                self.winIndex = 1
                self.itemIndex = self.todos_len[1]+1
            if k == key.CTRL_H and self.winIndex == 1:
                self.todo.moveTodo(self.itemIndex, 1)
                self.winIndex = 0
                self.itemIndex = self.todos_len[0]+1
        
        elif self.mode == "adding" or self.mode == "editing":
            if k == key.ESC:
                cursor.hide()
                self.mode = "todo"

            elif str(k) in punctuation or k in ascii_letters or k in digits or k == " ":
                self.todo.tfData += str(k)
            elif k == key.BACKSPACE:
                self.todo.tfData = self.todo.tfData[:-1]
            
            self.todo.tfWindow.editItem("text", self.todo.tfData)


            if k == key.ENTER:
                cursor.hide()
                if self.mode == "adding":
                    self.todo.progress.append([False, self.todo.tfData])
                elif self.mode == "editing":
                    self.todo.progress[self.itemIndex][1] = self.todo.tfData
                self.mode = "todo"

        

    def start(self):
        clear()
        self.todo.init()
        while self.running:
            self.wrap_indexes()
            if self.mode == "todo":
                self.todo.tfData = ""
                self.todo.tfWindow.editItem("text", self.todo.tfData)

                for win in self.windows:
                    win.draw()
            elif self.mode == "adding":
                self.todo.tfWindow.title = "Add Todo..."
                self.todo.drawTextField()

            elif self.mode == "editing":
                self.todo.tfWindow.title = "Edit Todo..."
                self.todo.drawTextField()
            # print(self.todo.tfData)
            self.handle_input()


if __name__ == "__main__":
    cursor.hide()
    main = Main()
    main.start()
    cursor.show()
