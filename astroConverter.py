from converts.converts import convert_hipparcos

data = convert_hipparcos("/home/laszlo/workspace/astroConverter/raw_data/hipparcos.txt")
print(data[0])
print(data[1])