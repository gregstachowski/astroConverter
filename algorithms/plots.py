import matplotlib.pyplot
import matplotlib.animation
import matplotlib.lines
import matplotlib.pyplot
from common import text_to_list


class Point(object):
    """has to be rewritten"""

    def __init__(self, x, y):
        self.plt = matplotlib.pyplot
        self.x_sequence = x
        self.y_sequence = y


class Plot(object):
    """has to be rewritten"""

    def __init__(self, list, master):
        self.master = master
        self.plt = matplotlib.pyplot
        self.x_sequence = list[0]
        self.y_sequence = list[1]

    def click(self, event):
        s = round(event.xdata,3)
        for x in self.x_sequence:
            if round(float(x),3) == s:
                print("bum")

    def create_plot(self):
        #self.plt.plot(self.x_sequence, self.y_sequence, 'bs-')
        self.fig = self.plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.plot(self.x_sequence, self.y_sequence, 'ro') # "ro"
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.click)
        self.master.windows.append(self)
        self.plt.show()
        
    def destroy(self):
        """try:
            self.master.windows.remove(self)
        except:
            print("TUTAJ")"""
        self.plt.close()
