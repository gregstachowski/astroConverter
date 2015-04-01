from widgets.menus import FileMenu, EditMenu, HelpMenu
from tkinter import Frame, Button, TOP, RIGHT, BOTTOM, X, Y, LEFT
from tkinter import Text, NONE, BOTH, YES, END
from tkinter import Scrollbar, VERTICAL, HORIZONTAL
from common import Info, loadfile, savefile, text_to_list
from algorithms.converts import Convert
from algorithms.plots import Plot


class MainMenu(object):

    def __init__(self, master, root, textfield):
        self.textField = textfield
        self.fileMenu = FileMenu(master, root, self.textField)
        self.editMenu = EditMenu(master, self.textField)
        self.helpMenu = HelpMenu(master)


class Toolbar(Frame):

    def __init__(self, master, textfield):
        self.textField = textfield
        Frame.__init__(self, master)
        self.b1, self.b2, self.b3 = None, None, None
        self.b4, self.b5 = None, None
        self._create_buttons()
        self.pack(side=TOP, fill=X)

    def _create_buttons(self):
        self.b1 = Button(self, text="Open File", command=self.textField.load)
        self.b1.pack(side=LEFT)
        self.b2 = Button(self, text="Save file", command=self.textField.save)
        self.b2.pack(side=LEFT)
        self.b3 = Button(self, text="Convert", command=self.textField.convert)
        self.b3.pack(side=LEFT)
        self.b4 = Button(self, text="Simple Plot", command=self.textField.plot)
        self.b4.pack(side=LEFT)
        self.b5 = Button(self, text="Live Plot", command=self.textField.liveplot)
        self.b5.pack(side=LEFT)


class TextField(Text):

    def __init__(self, master):
        self.master = master
        Text.__init__(self, master, width=50, height=30, wrap=NONE)
        self._create()
        self.pack(side=BOTTOM, fill=BOTH, expand=YES)

    def _create(self):
        ys = Scrollbar(self.master, orient=VERTICAL, command=self.yview)
        xs = Scrollbar(self.master, orient=HORIZONTAL, command=self.xview)
        ys.pack(side=RIGHT, fill=Y)
        xs.pack(side=BOTTOM, fill=X)
        self['ys'] = ys.set
        self['xs'] = xs.set

    def clear(self):
        self.delete(0.0, END)

    def get_text(self):
        return self.get(0.0, END)

    def insert_text(self, text):
        self.insert(0.0, text)

    def load(self):
        if len(self.get(0.0, END)) > 1:
            s = Info.askyesno("Are you sure?", "Text filed isn't empty.  Are you sure you want to load?"
                                               "You will loose your changes!")
            if not s:
                return
        self.clear()
        x = loadfile()
        if not x:
            return
        self.insert_text(x)

    def save(self):
        savefile(self.get_text())

    def convert(self):
        Convert(self)

    def plot(self):
        Plot(text_to_list(self.get_text())).create_plot()

    def liveplot(self):
        Plot.create_live_plot(self)
