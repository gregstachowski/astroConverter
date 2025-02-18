import copy
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RectangleSelector

from algorithms.tests import perftest
from common import myformat
from settings import Points
from widgets.periodbox import PeriodBox
from operator import itemgetter

import numpy as np
import io

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
        self.master = data  # it's needed for updating text_field #THINKOVER! MAYBE IT'S NOT NEEDED
        a = np.asarray(self.list).astype(np.float)
        self.unselected_points = np.asarray(list).astype(np.float)
        self.backup = np.copy(self.unselected_points)
        self.selected_points = np.array([[],[]])
        self.create_initial_graph()
        self.fig = None
        self.ax = None
        
    def draw_unselected_points(self):
        plt.axes(self.ax)
        self.ax.plot(self.unselected_points[0,:], self.unselected_points[1,:],
                     Points.base_config['unselected_point_line_type'], 
                     color=Points.base_config['unselected_point_color'],
                     )
        
    def draw_selected_points(self):
        plt.axes(self.ax)
        self.ax.plot(self.selected_points[0,:], self.selected_points[1,:],
                     Points.base_config['selected_point_line_type'],
                     color=Points.base_config['selected_point_color'],
                     )
        
    def set_labels(self):
        # self.ax.set_xlabel(Points.base_config['x_label'])
        # self.ax.set_ylabel(Points.base_config['y_label'])
        return

    def create_initial_graph(self):
        self.fig = plt.Figure()
        self.ax = plt.subplot(111)
        self.set_labels()
        self.draw_unselected_points()
        plt.subplots_adjust(bottom=0.2)
        ax = plt.gca()
        ax.invert_yaxis()
        axperiod = plt.axes([0.7, 0.04, 0.1, 0.075])
        axclear_select = plt.axes([0.81, 0.04, 0.1, 0.075])
        axrestore = plt.axes([0.59, 0.04, 0.1, 0.075])
        axsave = plt.axes([0.48, 0.04, 0.1, 0.075])
        axdel = plt.axes([0.37, 0.04, 0.1, 0.075])
        axreverse = plt.axes([0.26, 0.04, 0.1, 0.075])
        axselect = plt.axes([0.15, 0.04, 0.1, 0.075])
        bclr_select = Button(axclear_select, 'Clear \nselection')
        bclr_select.on_clicked(SelectHandler.clear_selection)
        bselect = Button(axselect, 'Select')
        bselect.on_clicked(self.start_selector)
        bdel = Button(axdel, 'Delete')
        bdel.on_clicked(SelectHandler.del_selected)
        bsave = Button(axsave, 'Save')
        bsave.on_clicked(self.saveme)
        breverse = Button(axreverse, "Reverse\nselection")
        breverse.on_clicked(self.reverse_selection)
        bperiod = Button(axperiod, "Period")
        bperiod.on_clicked(self.period_find)
        brestore = Button(axrestore, "Restore\npoints")
        brestore.on_clicked(self.restore_points)
        # ax.ticklabel_format(axis='x', style='plain',scilimits=(8,8)) #,useOffset=2456000)
        plt.show()

    def restore_points(self, event):
        self.unselected_points = np.copy(self.backup)
        self.selected_points = np.array([[],[]])
        self.redraw()

    def start_selector(self, event):
        # self.axselect.bselect.color('red')
        SelectHandler(event)

    def period_find(self, event):
        SelectHandler.clear_selection(event)
        PeriodBox(self, "Period")

    def reverse_selection(self, event):
        temporary = np.copy(self.unselected_points)
        self.unselected_points = np.copy(self.selected_points)
        self.selected_points = np.copy(temporary)
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

    # @perftest
    def update_text_field(self):
        self.master.clear()
        all = io.BytesIO()
        np.savetxt(all,self.unselected_points.T,"%.8f %.6f")
        self.master.insert_text(all.getvalue())

    # @perftest
    def redraw(self):
        self.update_text_field()
        plt.axes(self.ax)
        plt.ticklabel_format(axis='x', style='plain')
        plt.cla()
        self.draw_selected_points()
        self.draw_unselected_points()
        self.ax.invert_yaxis()
        plt.draw()

        
class SelectHandler(RectangleSelector):
    
    def __init__(self, event):
        RectangleSelector.__init__(self, Plot.plot.ax, onselect=self.onselect, useblit=True)
     
    # @perftest   
    def onselect(self, eclick, erelease):
        def is_in_range(xdata, ydata):
            x = float(xdata)
            y = float(ydata)
            if eclick.xdata <= x <= erelease.xdata or erelease.xdata <= x <= eclick.xdata:
                if eclick.ydata <= y <= erelease.ydata or erelease.ydata <= y <= eclick.ydata:
                    return True
            return False
        unsel = Plot.plot.unselected_points
        sel = Plot.plot.selected_points
        all_unsel_len = np.shape(unsel)[1]
        to_del = []
        for iter in range(all_unsel_len):
            if is_in_range(unsel[0,iter], unsel[1,iter]):
                to_del.append(iter)

        sel = np.hstack((sel,unsel[:,to_del]))
        to_del.sort(reverse=False)
        unsel = np.delete(unsel,to_del,1)
        # self.disconnect_events()
        Plot.plot.unselected_points = unsel
        Plot.plot.selected_points = sel
        Plot.plot.redraw()
                
    @staticmethod
    def clear_selection(event):
        """event is unused"""
        plot = Plot.plot
        plot.unselected_points = np.hstack((plot.unselected_points, plot.selected_points))
        plot.selected_points = np.array([[],[]])
        plot.redraw()
        
    @staticmethod
    def del_selected(event):
        plot = Plot.plot
        selected = plot.selected_points
        unselected = plot.unselected_points
        if len(selected[0]) == 0:
            return
        # making preperations for updating text field
        # deleting points
        plot.selected_points = np.array([[],[]])
        plot.redraw()
