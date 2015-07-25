import copy
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RectangleSelector

from algorithms.tests import perftest
from common import myformat
from settings import Points
from widgets.periodbox import PeriodBox


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

    def __init__(self, list, data):
        self.list = list
        Plot.plot = self
        self.backup = copy.deepcopy(list)
        self.master = data  # it's needed for updating text_field #THINKOVER! MAYBE IT'S NOT NEEDED
        self.unselected_points = list
        self.selected_points = [[], []]
        self.create_initial_graph()
        self.fig = None
        self.ax = None
        
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
        self.fig = plt.Figure()
        self.ax = plt.subplot(111)
        self.set_labels()
        self.draw_unselected_points()
        plt.subplots_adjust(bottom=0.2)
        ax = plt.gca()
        ax.invert_yaxis()
        axdel = plt.axes([0.7, 0.04, 0.1, 0.075])
        axselect = plt.axes([0.81, 0.04, 0.1, 0.075])
        axclear_select = plt.axes([0.59, 0.04, 0.1, 0.075])
        bclr_select = Button(axclear_select, 'Clear \nselection')
        bclr_select.on_clicked(SelectHandler.clear_selection)
        bselect = Button(axselect, 'Select')
        bselect.on_clicked(SelectHandler)
        bdel = Button(axdel, 'Delete')
        bdel.on_clicked(SelectHandler.del_selected)
        axsave = plt.axes([0.48, 0.04, 0.1, 0.075])
        bsave = Button(axsave, 'Save')
        bsave.on_clicked(self.saveme)
        axreverse = plt.axes([0.37, 0.04, 0.1, 0.075])
        breverse = Button(axreverse, "Reverse\nselection")
        breverse.on_clicked(self.reverse_selection)
        axperiod = plt.axes([0.26, 0.04, 0.1, 0.075])
        bperiod = Button(axperiod, "Period")
        bperiod.on_clicked(self.period_find)
        axrestore = plt.axes([0.15, 0.04, 0.1, 0.075])
        brestore = Button(axrestore, "Restore\npoints")
        brestore.on_clicked(self.restore_points)
        plt.show()

    def restore_points(self, event):
        self.selected_points = [[], []]
        self.unselected_points = copy.deepcopy(self.backup)
        self.redraw()

    def period_find(self, event):
        SelectHandler.clear_selection(event)
        PeriodBox(self, "Period", "enter period:")  # FUCK THIS SHIT ....

    def reverse_selection(self, event):
        temporary = self.unselected_points
        self.unselected_points = self.selected_points
        self.selected_points = temporary
        Plot.plot.redraw()
        
    def saveme(self, event):
        directory = self.master.directory
        if not directory:
            directory = filedialog.asksaveasfilename()
            self.master.directory = directory  # setting new directory for textField
            extent = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
            plt.savefig(directory, bbox_inches=extent.expanded(1.3, 1.2))
            return
        directory = directory.split("/")
        name = directory[-1]
        name = name.split(".")
        del name[-1]
        name.append(".png")
        name = "".join(name)
        del directory[-1]
        directory.append(name)
        directory = "/".join(directory)
        extent = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(directory, bbox_inches=extent.expanded(1.3, 1.2))

    @perftest
    def redraw(self):
        plt.axes(self.ax)
        plt.cla()
        self.draw_selected_points()
        self.draw_unselected_points()
        plt.draw()

        
class SelectHandler(RectangleSelector):
    
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
        plot = Plot.plot
        selected = plot.selected_points
        unselected = plot.unselected_points
        for iter in range(len(plot.selected_points[0])):
            unselected[0].append(selected[0][iter])
            unselected[1].append(selected[1][iter])
        plot.selected_points = [[], []]
        plot.redraw()
        
    @staticmethod
    def del_selected(event):
        plot = Plot.plot
        selected = plot.selected_points
        unselected = plot.unselected_points
        if len(selected[0]) == 0:
            return
        # making preperations for updating text field
        l = len(unselected[0])
        out = []
        for iter in range(l):
            out.append([str(unselected[0][iter]), str(unselected[1][iter])])
        # updating text_field
        plot.master.clear()
        plot.master.insert_text(myformat(out))
        # deleting points
        plot.selected_points = [[], []]
        plot.redraw()
