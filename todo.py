import shutil
from window import Window

class Todo:
    
    def __init__(self) -> None:
        self.w = self.h = 0
        self.progressWindow = Window()
        self.doneWindow = Window()
        self.tfWindow = Window()
        self.progress = []
        self.tfData = ""
    
    def readtxt(self):
        with open("data.txt", "r") as f:
            data = f.read()
            return eval(data)
    
    def writetxt(self, data_write):
        with open("data.txt", "w") as f:
            f.write(str(data_write))


    def init(self):
        self.w, self.h = shutil.get_terminal_size()
        self.todos = self.readtxt()
        self.progressWindow.init([1,1], w=self.w//2 - 1, h=self.h, title="In Progress")
        self.doneWindow.init([int(self.w//2), 1], w=self.w//2, h=self.h, title="Done!")
        self.tfWindow.init([self.w//4, self.h//2], int(self.w//2), 1, "Enter Todo...")

        self.done = []
        self.progress = []

        for todo in self.todos:
            if todo[0]:
                self.done.append(todo)
            else:
                self.progress.append(todo)
        self.progressWindow.addItem("list", self.progress, "left", True)
        self.doneWindow.addItem("list", self.done, "left", True)
        self.tfWindow.addItem("text", self.tfData, "left", False)

    def drawTextField(self):
        # tf = Text Field
        self.tfWindow.draw()
        

    def drawTodos(self):
        self.progressWindow.draw()
        self.doneWindow.draw()

    def moveTodo(self, index, move_from):
        if move_from == 0:
            self.done.append(self.progress[index])
            self.progress.pop(index)
        else:
            self.progress.append(self.done[index])
            self.done.pop(index)
        
    def savetxt(self):
        toSave = []

        for todo in self.progress:
            todo[0] = False
            toSave.append(todo)

        for todo in self.done:
            todo[0] = True
            toSave.append(todo)

        self.writetxt(toSave)

