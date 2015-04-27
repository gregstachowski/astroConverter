import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RectangleSelector
from time import time, sleep
from algorithms.tests import perftest
from common import myformat
from settings import Points

# TODO:
# point finder \/
# change color of chosen point \/
# delete points \/
# clear point selection (in case of errors) \/
# update text_field (COULD BE TRICKY!) \/
# make use of Points.base_config. Best if everything will be in settings.py \/
# names, text etc in graphs \/
# add names for axes \/

# BUGS:
# axes titles are dissapearing after selecting points. Add updates...

class Plot(object):
    
    plot = None

    def __init__(self, list, master):
        self.list = list
        Plot.plot = self
        self.master = master #it's needed for updating text_field #THINKOVER! MAYBE IT'S NOT NEEDED
        self.unselected_points = list
        self.selected_points = [[],[]]
        self.create_initial_graph()
        
    def draw_unselected_points(self):
        plt.axes(self.ax)
        self.ax.plot(self.unselected_points[0], self.unselected_points[1],
                     Points.base_config['unselected_point_line_type'], 
                     color=Points.base_config['unselected_point_color'],
                     )
        
    def draw_selected_points(self):
        plt.axes(self.ax)
        self.ax.plot(self.selected_points[0], self.selected_points[1],
                    Points.base_config['selected_point_line_type'],
                    color=Points.base_config['selected_point_color'],
                    )
        
    def set_labels(self):
        self.ax.set_xlabel(Points.base_config['x_label'])
        self.ax.set_ylabel(Points.base_config['y_label'])


    def create_initial_graph(self):
        self.ax = plt.subplot(111)
        self.set_labels()
        self.draw_unselected_points()
        plt.subplots_adjust(bottom=0.2)
        ax = plt.gca()
        ax.invert_yaxis()
        axdel = plt.axes([0.7, 0.05, 0.1, 0.075])
        axselect = plt.axes([0.81, 0.05, 0.1, 0.075])
        axclear_select = plt.axes([0.59, 0.05, 0.1, 0.075])
        bclr_select = Button(axclear_select, 'Clear \nselection')
        bclr_select.on_clicked(Select_handler.clear_selection)
        bselect = Button(axselect, 'Select')
        bselect.on_clicked(Select_handler)
        bdel = Button(axdel, 'Delete')
        bdel.on_clicked(Select_handler.del_selected)
        plt.show()

    @perftest
    def redraw(self):
        plt.axes(self.ax)
        plt.cla()
        self.draw_selected_points()
        self.draw_unselected_points()
        plt.draw()

        
class Select_handler(RectangleSelector):
    
    def __init__(self, event):
        RectangleSelector.__init__(self, Plot.plot.ax, onselect=self.onselect)
     
    @perftest   
    def onselect(self, eclick, erelease):
        def is_in_range(xdata, ydata):
            x = float(xdata)
            y = float(ydata)
            if eclick.xdata <= x <= erelease.xdata or erelease.xdata <= x <= eclick.xdata:
                if eclick.ydata <= y <= erelease.ydata or erelease.ydata <= y <= eclick.ydata:
                    return True
        unsel = Plot.plot.unselected_points
        sel = Plot.plot.selected_points
        all_unsel_len = len(unsel[0])
        to_del = []
        for iter in range(all_unsel_len):
            xcord = unsel[0][iter]
            ycord = unsel[1][iter]
            if is_in_range(xcord, ycord):
                sel[0].append(xcord)
                sel[1].append(ycord)
                to_del.append(iter)
        to_del.sort(reverse=True)
        for index in to_del:
            del unsel[0][index]
            del unsel[1][index]
        self.disconnect_events()
        Plot.plot.redraw()
                
    @staticmethod
    def clear_selection(event):
        """event is unused"""    
        for iter in range(len(Plot.plot.selected_points[0])):
            Plot.plot.unselected_points[0].append(Plot.plot.selected_points[0][iter])
            Plot.plot.unselected_points[1].append(Plot.plot.selected_points[1][iter])
        Plot.plot.selected_points = [[],[]]
        Plot.plot.redraw()
        
    @staticmethod
    def del_selected(event):
        if len(Plot.plot.selected_points[0]) == 0: return
        #making preperations for updating text field
        unsel = Plot.plot.unselected_points
        l = len(unsel[0])
        out = []
        for iter in range(l):
            out.append([unsel[0][iter], unsel[1][iter]])
        #updating text_field
        Plot.plot.master.clear()
        Plot.plot.master.insert_text(myformat(out))
        #deleting points
        Plot.plot.selected_points = [[],[]]
        Plot.plot.redraw()
        
        
        
        
        
        