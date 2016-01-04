import tkinter as Tk
from settings import app_name
from tkinter import Menu, Button
import numpy as np

import sys

from gui.canvas_plot import CanvasPlot


class MainWindow(CanvasPlot):
    
    def __init__(self):
        self.tk_root_ref = Tk.Tk()
        CanvasPlot.__init__(self)
        
    def initial_config(self):
        self.tk_root_ref.wm_title(app_name)
        self.__create_topmenu()
        
        
    def start(self):
        self.tk_root_ref.mainloop()
        
    def new_plot(self):
        dir = Tk.filedialog.askopenfilename()
        x, y = np.loadtxt(dir, usecols=(0, 1), unpack=True)
        self.figure.gca().clear()
        self.subplot.plot(x, y, 'o')
        self.subplot.set_title(dir)
        self.subplot.set_xlabel('x')
        self.subplot.set_ylabel('y')
        self.canvas.show()
        
    def __create_topmenu(self):
        self.menubar = Menu(self.tk_root_ref)
        
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New plot", command=self.new_plot)
        self.filemenu.add_command(label="Exit", command=sys.exit)
        
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.tk_root_ref.config(menu=self.menubar)
