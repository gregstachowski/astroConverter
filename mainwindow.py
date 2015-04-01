from tkinter import Tk, Menu
from widgets.widgets import MainMenu, Toolbar, TextField
import settings


class MrRoot(Tk):
    """Main window"""

    def __init__(self):
        Tk.__init__(self)
        self.windows = []
        self.mainMenu = Menu(self)
        self.config(menu=self.mainMenu)
        self.textField = None
        self._create_widgets()

    def _create_widgets(self):
        self.textField = TextField(self)
        MainMenu(self.mainMenu, self, self.textField)
        Toolbar(self, self.textField)

    def configure(self):
        self.title(settings.title + settings.version)
        self.geometry(settings.size)
        
    def destroy(self):
        #print(self.windows)
        while len(self.windows) > 0:
            try:
                for window in self.windows:
                    window.destroy()
                    self.windows.remove(window)
            except AttributeError:
                print("AttributeError in destroy mainwindow")
        #print(self.windows)
        Tk.destroy(self)
        

if __name__ == "__main__":
    MrRoot()