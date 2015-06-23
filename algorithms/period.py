from algorithms.variability import VariabilityTest

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
        self.period = period
        self.tolerance = 0.1
        
    def calculate(self):
        for point in self.points:
            jd = point.jd
            part1 = calculate_period(float(jd), self.period)
            part2 = int(calculate_period(float(jd), self.period))
            point.jd = part1 - part2
        return self.points
    
    
class ExperimentalPeriod(object):
    
    def __init__(self, times, magnitudo):
        self.times = times
        self.magnitudo = magnitudo
        self.min = 0
        self.max = 1
        self.step = 0.0001
        self.calculate()
        
    def calculate(self):
        max = 0
        for i in range(1, 10000):
            points = Period(self.times, self.magnitudo, 0.9042).calculate()
            t = []
            m = []
            for p in points:
                t.append(float(p.jd))
                m.append(float(p.magnitudo))
            result = VariabilityTest(m, t, 2).calculate()
            if result > max:
                max = i
                print("%s - %s" % (result, i))
            #print(i/10000 * 100)
        print(max)
        