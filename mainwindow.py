from tkinter import Tk, Menu
from _tkinter import TclError

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
        to_destroy = []
        for x in range(len(self.windows)):
            try:
                self.windows[x - 1].destroy()
                to_destroy.append(self.windows[x - 1])
            except TclError:
                to_destroy.append(self.windows[x - 1])
        for x in to_destroy:
            self.windows.remove(x)
        print(self.windows)
        Tk.destroy(self)


if __name__ == "__main__":
    MrRoot()
