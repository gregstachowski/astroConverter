from tkinter import Tk, Menu
from widgets.widgets import MainMenu, Toolbar, TextField
import settings


class MrRoot(Tk):

    others = []

    def __init__(self):
        Tk.__init__(self)
        self.mainMenu = Menu(self)
        self.config(menu=self.mainMenu)
        self.textField = None
        self.create_widgets()

    def create_widgets(self):
        self.textField = TextField(self)
        MainMenu(self.mainMenu, self, self.textField)
        Toolbar(self, self.textField)

    def configure(self):
        self.title(settings.title + settings.version)
        self.geometry(settings.size)


if __name__ == "__main__":
    MrRoot()
    print(MrRoot.root)