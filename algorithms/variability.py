import sys

def in_range(number, lower_range, upper_range):
    if number <= upper_range and number >= lower_range:
        return True
    return False
    
    
def test_equal(chunk, size):
    if len(chunk) == size:
        return True
    return False

def save(mag, var):
    file = open("mag_var.txt", "a")
    file.write(str(mag) + "\t" + str(var) + "\n")
    file.close()


def remove_empty(data):
    """Removes empty items from list"""
    out = []
    for item in data:
        if item == '': continue
        out.append(item)
    return out


def cut_data(data):
    """cuts two-row data into two seperate lists. Items are formatted as float"""
    out = [[], []]
    data = data.split("\n")
    for line in data:
        line = line.split(" ")
        line = remove_empty(line)
        try:
            out[0].append(float(line[0]))
            out[1].append(float(line[1]))
        except IndexError:
            pass
    file = open("test.txt", "w")
    for i in out[1]: # DELETE
        file.write(str(i))
        file.write("\n")
    file.close()
    return out


def load_file(file):
    file = open(file, "r")
    data = file.read()
    file.close()
    return data


def create_points(data):
    """creates points objects. returns array of points"""
    points = []
    for i in range(len(data[0])):
        points.append(Point(data[0][i], data[1][i]))
    return points


def create_chunks(points, deviation_weight, max_points = 5):
    """creates chunks. 
    Returns arrays of points - chunks"""
    #max_points = round(len(points)/10)
    chunks = []
    temp_array = []
    for i in range(len(points)):
        if len(temp_array) == max_points: # points in one chunk
            chunks.append(Chunk(temp_array, deviation_weight))
            temp_array = []
        temp_array.append(points[i])
    if test_equal(temp_array, max_points): #  making sure my chunks are equal sized
        chunks.append(Chunk(temp_array, deviation_weight)) # adding last points into last chunk
    return chunks
    

class Point(object):
    
    def __init__(self, time, magnitudo):
        self.time = time
        self.magnitudo = magnitudo
        self.deviation = None #calculate using mean
        self.squared_deviation = None #calculate using deviation
        
    def calculate_deviation(self, mean):
        self.deviation = self.magnitudo - mean
    
    def calculate_squared_deviation(self):
        self.squared_deviation = self.deviation * self.deviation
        
    def __repr__(self):
        return "Time: %s\tMagnitudo: %s" % (self.time, self.magnitudo)
        

class Chunk(object):
    
    def __init__(self, points_array, deviation_weight):
        self.deviation_weight = deviation_weight
        self.points = points_array
        self.mag_mean = None
        self.mag_variance = None
        self.standard_deviation = None
        self.lower_range = None
        self.higher_range = None
    
    def calculate_mean_mag(self):
        mags = []
        for point in self.points:
            mags.append(point.magnitudo)
        self.mag_mean = sum(mags)/len(mags)
    
    def calculate_variance_mag(self):
        mags = []
        for point in self.points:
            point.calculate_deviation((self.mag_mean))
            point.calculate_squared_deviation()
            mags.append(point.squared_deviation)
        self.mag_variance = sum(mags)/len(mags)
        
    def calculate_standard_deviation(self):
        self.standard_deviation = self.mag_variance**(1/2)
        
    def calculate_ranges(self):
        self.lower_range = self.mag_mean - self.deviation_weight * self.standard_deviation
        self.higher_range = self.mag_mean + self.deviation_weight * self.standard_deviation
        
    def __repr__(self):
        return str(self.standard_deviation)

    @staticmethod
    def remove_points(chunk):
        #print("Starting points: %s" % chunk.points)
        max_range = chunk.mag_mean + chunk.standard_deviation
        min_range = chunk.mag_mean - chunk.standard_deviation
        for point in chunk.points:
            if point.magnitudo > max_range or point.magnitudo < min_range:
                chunk.points.remove(point)
        #print("Ending points: %s" % chunk.points)
        
    @staticmethod
    def calculate_all(chunks):
        for chunk in chunks:
            chunk.calculate_mean_mag()
            chunk.calculate_variance_mag()
            chunk.calculate_standard_deviation()
            chunk.calculate_ranges()
            
    @staticmethod
    def range_test(testing_chunk, second_chunk):
        if in_range(testing_chunk.mag_mean, second_chunk.lower_range, second_chunk.higher_range):
            return True
        return False
    
def tester(points, size, deviation_weight):
    chunks = create_chunks(points, deviation_weight, size)
    Chunk.calculate_all(chunks)
    for chunk in chunks:
        Chunk.remove_points(chunk)
    Chunk.calculate_all(chunks)
    """for c in chunks:
        print(c.standard_deviation)
    print("="*25)"""
    length = len(chunks)
    failed_mean = 0
    #print(length)
    for i in range(0, length-1):
        testing_chunk = chunks[i]
        next_chunk = chunks[i+1]
        if not Chunk.range_test(testing_chunk, next_chunk):
            failed_mean += 1
    #print(failed_mean)
    if failed_mean:
        return 1
    return 0

class VariabilityTest(object):
    
    def __init__(self, time, magnitudo, deviation_weight = 1, percentage_condition = 20):
        """accepts two arrays: times and magnitudo
        returns True if variability is found
        return False if variability isn't found"""
        self.time = time
        self.magnitudo = magnitudo
        self.deviation_weight = deviation_weight
        self.percentage_condition = percentage_condition
        self.min_range = None
        self.max_range = None
        self.points = None
        
    def calculate(self):
        self.points = create_points([self.time, self.magnitudo])
        self.min_range = 5
        self.max_range = round(len(self.points)/5)
        failed = 0
        for i in range(self.min_range, self.max_range):
            failed += tester(self.points, i, self.deviation_weight)
        return failed/(self.max_range-self.min_range) * 100
        if (failed/(self.max_range-self.min_range) * 100) > self.percentage_condition:
            return True
        return False

def main(args, percentage_condition = 20):
    if not args:
        print("Choose files")
        return
    for file in args:
        data = load_file(file)
        data = cut_data(data)
        points = create_points(data)
        min = 5 #minimal number of points in one chunk
        max  = int(round(len(points)/5)) # max points in one chunk
        failed = 0
        for i in range(min, max):
            failed += tester(points, i, 1)
        score = failed/(max-min) * 100
        print(file)
        print("Score: %s%%" % score)
        print("Failed: %s out of %s tests" % (failed, max-min) )
        if score >= percentage_condition: # if more than 20% of tests failed, the star is considered as variable
            print("Variability: True")
        else: print("Variability: False")
        print("="*20)
    
if __name__ == '__main__':
    args = sys.argv
    args = args[1:]
    main(args)