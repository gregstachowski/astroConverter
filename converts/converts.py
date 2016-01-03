import numpy as np

def convert_hipparcos(file_dir):
    """ loads *.txt from file and returns 0 and 1 column
        adds 2440000 to 0 columns, to create JD format"""
        
    raw_data = np.loadtxt(file_dir, skiprows=1,
                     delimiter="|")
    
    hjd = raw_data[:,0]
    mag = raw_data[:,1]
    jd = hjd + 2440000
    return (jd, mag)