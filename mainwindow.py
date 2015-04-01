from tkinter import Tk, Menu
from widgets.widgets import MainMenu, Toolbar, TextField
import settings


class MrRoot(Tk):
    """Main window"""

    def __init__(self):
        Tk.__init__(self)
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


if __name__ == "__main__":
    MrRoot()