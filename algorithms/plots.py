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

    def __init__(self, list):
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
        self.ax.plot(self.x_sequence, self.y_sequence, 'bs-') # "ro"
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.click)
        self.plt.show()

    @staticmethod
    def create_live_plot(master):
        fig = matplotlib.pyplot.figure('bs-')
        ax1 = fig.add_subplot(1, 1, 1)

        def animate(i):
            ax1.cla()
            text = master.get_text()
            l = text_to_list(text)
            try:
                ax1.plot(l[0], l[1])
            except ValueError:
                pass

        matplotlib.animation.FuncAnimation(fig, animate, interval=1000)
        matplotlib.pyplot.show()
