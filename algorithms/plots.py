import matplotlib.pyplot as plt


class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = 'b'
        
    def __str__(self):
        return str(self.x) + " - " + str(self.y)
    

class Plot(object):
    """
    *******************
    HAS TO BE REWRITTEN
    *******************
    """

    def __init__(self, list, master):
        self.master = master
        self.points = []
        self.create_points(list)
        self.create_graph()
    
    def create_points(self, list):
        for x in range(len(list[0])):
            x_cord = list[0][x-1]
            y_cord = list[1][x-1]
            self.points.append(Point(x_cord, y_cord))
            
    def create_graph(self):
        for p in self.points:
            plt.plot(p.x, p.y, 'o', color=p.color)
        plt.show()
        
        