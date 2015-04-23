import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RectangleSelector
from time import time, sleep
# TODO:
# point finder
# change color of chosen point
# delete points
# clear point selection (in case of errors)
# update text_field (COULD BE TRICKY!)

class Point(object):
    
    base_config={'color': 'b',
                 'select_color': 'r'}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = Point.base_config['color']
        
    def __str__(self):
        return str(self.x) + " - " + str(self.y) + "Color: " + self.color
    
    @staticmethod
    def delete_points(event):
        todelete = []
        for point in Plot.plot.points:
            if point.color == 'r':
                todelete.append(point)
        for td in todelete:
            Plot.plot.points.remove(td)
        Plot.plot.redraw()
    

class Plot(object):
    """
    *******************
    HAS TO BE REWRITTEN
    *******************
    """
    plot = None # Remember to update reference. It may be important!

    def __init__(self, list, master):
        #print(list)
        self.list = list
        Plot.plot = self
        self.master = master #it's needed for updating text_field
        self.points = []
        self.create_points(list)
        self.create_graph()
        
    
    def create_points(self, list):
        for x in range(len(list[0])):
            x_cord = list[0][x-1]
            y_cord = list[1][x-1]
            self.points.append(Point(x_cord, y_cord))
            
    def get_list_of_cords(self):
        cordsx = []
        cordsy = []
        for point in self.points:
            cordsx.append(point.x)
            cordsy.append(point.y)
        return (cordsx, cordsy)
            
    def create_graph(self):
        self.ax = plt.subplot(111)
        #for p in self.points:
        #    plt.plot(p.x, p.y, 'o', color=p.color)
        cords = self.get_list_of_cords()
        plt.plot(cords[0], cords[1], 'o', color='b')
        plt.subplots_adjust(bottom=0.2)
        axdel = plt.axes([0.7, 0.05, 0.1, 0.075])
        axselect = plt.axes([0.81, 0.05, 0.1, 0.075])
        axclear_select = plt.axes([0.59, 0.05, 0.1, 0.075])
        bclr_select = Button(axclear_select, 'Clear \nselection')
        bclr_select.on_clicked(Select_handler.clear_selection)
        bselect = Button(axselect, 'Select')
        bselect.on_clicked(Select_handler)
        bdel = Button(axdel, 'Delete')
        bdel.on_clicked(Point.delete_points)
        plt.show()
        
    def redraw(self):
        plt.axes(self.ax)
        plt.cla()
        for p in self.points:
            self.ax.plot(p.x, p.y, 'o', color=p.color)
        plt.draw()
        
        
class Select_handler(RectangleSelector):
    
    def __init__(self, event):
        RectangleSelector.__init__(self, Plot.plot.ax, onselect=self.onselect)
        
    def onselect(self, eclick, erelease):
        def is_in_range(point):
            x = float(point.x)
            y = float(point.y)
            if eclick.xdata <= x <= erelease.xdata or erelease.xdata <= x <= eclick.xdata:
                if eclick.ydata <= y <= erelease.ydata or erelease.ydata <= y <= eclick.ydata:
                    return True
        print("Eclick: %s - %s" %(eclick.xdata, eclick.ydata))
        print("Erelease: %s - %s" % (erelease.xdata, erelease.ydata))
        t1 = time()
        for point in Plot.plot.points:
            if is_in_range(point):
               point.color = 'r'
        t2 = time()
        Plot.plot.redraw()
        t3 = time()
        print("Points: %s\nLoop: %s\nRedraw: %s" %(len(Plot.plot.points), t2-t1, t3-t2))
        self.set_active(False)
        
    @staticmethod
    def clear_selection(event):
        """event is unused"""    
        for point in Plot.plot.points:
            point.color = 'b'
        Plot.plot.redraw()
        
        
        
        
        
        
        
        