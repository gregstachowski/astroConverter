import matplotlib
matplotlib.use('TkAgg')

import sys

from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import TOP, BOTH, LEFT, Button

class CanvasPlot(object):
    
    def __init__(self):
        self.figure = Figure()
        self.subplot = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.tk_root_ref)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.tk_root_ref)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        
        self.quitbutton = Button(master=self.tk_root_ref,
                                 text='Quit button',
                                 command = sys.exit)
        self.quitbutton.pack(side=LEFT)