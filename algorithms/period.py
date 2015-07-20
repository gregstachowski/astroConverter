from algorithms.variability import VariabilityTest, cut_data
#from variability import VariabilityTest, cut_data
from time import time

def create_points(jd, mag):
    points = []
    for i in range(len(jd)):
        points.append(Point(jd[i], mag[i]))
    return points


def calculate_period(jd, period, mo = 2450000):
    return (jd - mo)/period


class Point(object):
    
    def __init__(self, jd, magnitudo):
        self.jd = jd
        self.magnitudo = magnitudo
    
    
class Period(object):
    
    def __init__(self, times, magnitudo, period = 0.9042):
        self.points = create_points(times, magnitudo)
        self.secondPartOfPoints = None
        self.period = period
        self.tolerance = 0.1
        
    def calculate(self):
        for point in self.points:
            jd = point.jd
            part1 = calculate_period(float(jd), self.period)
            part2 = int(calculate_period(float(jd), self.period))
            point.jd = part1 - part2
        self.addSecondPartOfPoints()
        return self.points

    def addSecondPartOfPoints(self):
        temporaryPoints = []
        for point in self.points:
            temporaryPoints.append(Point(point.jd, point.magnitudo))
        for point in self.points:
            point.jd += self.period
        self.points.extend(temporaryPoints)
    
    
class ExperimentalPeriod(object):
    
    def __init__(self, times, magnitudo):
        self.times = times
        self.magnitudo = magnitudo
        self.min = 0
        self.max = 1
        self.step = 0.0001
        self.calculate()
        
    def calculate_ten_times(self):
        for i in range(1, 10):
            points = Period(self.times, self.magnitudo, i/10000).calculate()
            t = []
            m = []
            for p in points:
                t.append(float(p.jd))
                m.append(float(p.magnitudo))
            new_result = VariabilityTest(m, t, 2).calculate()
        
    def calculate(self):
        per = 0
        result = 0
        t1 = time()
        self.calculate_ten_times()
        avg_time = time() - t1
        print("It will take %s sec in avg" % (avg_time * 1000))
        for i in range(1, 10000):
            points = Period(self.times, self.magnitudo, i/10000).calculate()
            t = []
            m = []
            for p in points:
                t.append(float(p.jd))
                m.append(float(p.magnitudo))
            new_result = VariabilityTest(m, t, 2).calculate()
            if new_result > result:
                per = i/10000
                result = new_result
                print("Current per: %s\nCurrent result: %s" % (per, result))
                #print("%s - %s" % (result, i))
        print("Per: %s\nResult: %s" % (per, result))
    
        
if __name__ == '__main__':
    file = open("/home/laszlo/workspace/astroConverter/mats/AC-Cru.txt", "r")
    data = file.read()
    data = cut_data(data)
    t1 = time()
    exp = ExperimentalPeriod(data[0], data[1])
    print("It took %s seconds" % (time() - t1))
    