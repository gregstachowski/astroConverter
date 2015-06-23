from widgets.menus import FileMenu, EditMenu, HelpMenu
from tkinter import Frame, Button, TOP, RIGHT, BOTTOM, X, Y, LEFT
from tkinter import Text, NONE, BOTH, YES, END
from tkinter import Scrollbar, VERTICAL, HORIZONTAL
from common import Info, loadfile, savefile, text_to_list, quicksavefile, cut_data
from algorithms.converts import Convert
from algorithms.plots import Plot
from algorithms.variability import VariabilityTest


class MainMenu(object):

    def __init__(self, data, root, textfield):
        self.textField = textfield
        self.fileMenu = FileMenu(data, root, self.textField)
        self.editMenu = EditMenu(data, self.textField)
        self.helpMenu = HelpMenu(data)


class Toolbar(Frame):

    def __init__(self, data, textfield):
        self.textField = textfield
        Frame.__init__(self, data)
        self.b1, self.b2, self.b3 = None, None, None
        self.b4, self.b5, self.b6 = None, None, None
        self._create_buttons()
        self.pack(side=TOP, fill=X)

    def _create_buttons(self):
        self.b1 = Button(self, text="Open File", command=self.textField.load)
        self.b1.pack(side=LEFT)
        self.b2 = Button(self, text="Quick Save file",
                         command=self.textField.quick_save)
        self.b2.pack(side=LEFT)
        self.b3 = Button(self, text="Convert", command=self.textField.convert)
        self.b3.pack(side=LEFT)
        self.b4 = Button(self, text="Simple Plot", command=self.textField.plot)
        self.b4.pack(side=LEFT)
        self.b5 = Button(self, text="VariabilityTest", command=self.textField.variability)
        self.b5.pack(side=LEFT)


class TextField(Text):

    def __init__(self, data):
        self.master = data
        Text.__init__(self, self.master, width=50, height=30, wrap=NONE)
        self._create()
        self.directory = None
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
        x = loadfile() #here we got tuple (directory, text)
        if not x:
            return
        self.directory = x[0]
        self.insert_text(x[1])

    def save(self):
        savefile(self.get_text())

    def quick_save(self):
        quicksavefile(self.directory, self.get_text())

    def convert(self):
        Convert(self, self.master)

    def plot(self):
        Plot(text_to_list(self.get_text()), self)
    
    def variability(self):
        data = cut_data(self.get_text())
        varability = VariabilityTest(data[0], data[1], deviation_weight = 1, percentage_condition=0)
        test = varability.calculate()
        Info.message("VariabilityTest", "Variability: %s" % test)
