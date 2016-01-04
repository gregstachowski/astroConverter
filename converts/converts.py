from numpy import loadtxt

def convert_hipparcos(file_dir):
    """ loads *.txt from file and returns 0 and 1 column
        adds 2440000 to 0 columns, to create JD format"""
        
    hjd, mag = loadtxt(file_dir, skiprows=1,
                     delimiter="|", usecols=(0, 1),
                     unpack=True)
    jd = hjd + 2440000
    return (jd, mag)

def convert_asas(file_dir):
    """ loads *.txt from file and returns 
    time and magnitudo column with the smallest
    measurement error """
    raw_data = loadtxt(file_dir, usecols=(0, 1))
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    data = convert_hipparcos("/home/laszlo/workspace/astroConverter/raw_data/hipparcos.txt")
    print(data)
    plt.plot(data[0], data[1], 'o')
    plt.show()