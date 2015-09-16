import tkinter.messagebox
import tkinter.filedialog

from astropy.io import fits
import numpy
from operator import itemgetter


class Info():
    """Info-class for pop-up messages"""

    @staticmethod
    def notimplemented():
        tkinter.messagebox.showinfo("Not implemented", "Not implemented yet")

    @staticmethod
    def about():
        tkinter.messagebox.showinfo("About", "About")

    @staticmethod
    def askyesno(tit, tex):
        return tkinter.messagebox.askyesno(tit, tex)

    @staticmethod
    def message(msg1, msg2):
        tkinter.messagebox.showinfo(msg1, msg2)

    @staticmethod
    def license():
        pass


def loadfile():
    """loads file. Has build-in file format recognize system
    returns tuple(directory, text)"""
    try:
        x = tkinter.filedialog.askopenfilename()
    except TypeError:
        return
    if not x:
        return
    y = x.split(".")
    if y[-1] == "fits":
        # TODO: this is extremely stupid and dummy. Create new function for converting
        # add proper formating etc
        hdulist = fits.open(x)
        tbdata = hdulist[1].data
        a = tbdata.field('TMID')/86400.0 + 2453005.5
        b = 15 - 2.5*numpy.log10(tbdata.field('TAMFLUX2'))
        out = ""
        for i in range(len(a)):
            out += str(a[i]) + " " * 5 + str(b[i]) + "\n"
        return (x, out)
    else:
        file = open(x)
        y = file.read()
        file.close()
        s = (x, y)
        return s


def quicksavefile(directory, text, format=".out"):
    """saves file in given directory in fiven format"""
    print(text)
    print(directory)
    directory = directory.split(".")
    del directory[-1]
    directory.append(format)
    s = "".join(directory)
    file = open(s, "w")
    file.write(text)
    file.close()


def remove_empty(data):
    """Removes empty items from list"""
    out = []
    for item in data:
        if item == '':
            continue
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
    for i in out[1]:  # DELETE
        file.write(str(i))
        file.write("\n")
    file.close()
    return out


def savefile(text):
    """opens tkinter filedialog to save file"""
    file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if not file:
        return
    file.write(text)
    file.close()


def text_to_list(text):
    """creates to-plot-list from string"""
    text = text.split("\n")
    mylist = []
    a, b = [], []
    x = " "
    for el in text:
        temp = []
        el = el.split()
        for pos in el:
            if len(pos) == 0:
                continue
            if x not in pos:
                temp.append(pos)
        try:
            a.append(temp[0])
            b.append(temp[1])
        except IndexError:
            pass
    a = del_empty(a)
    b = del_empty(b)
    mylist.append(a)
    mylist.append(b)
    return mylist


def del_empty(list):
    """deletes empty elements in lists"""
    for x in range(len(list)):
        if len(list[x - 1]) == 0:
            del list[x - 1]
    return list


def del_empty_space(list):
    """deletes empty elements with "space" in it"""
    for x in range(len(list)):
        if " " in list[x - 1]:
            del list[x - 1]
    return list


def clear_list(list):
    """ clears "" and " " in list """
    for x in range(len(list)):
        try:
            list.remove("")
        except ValueError:
            pass
        try:
            list.remove(" ")
        except ValueError:
            pass
    return list


def get_without(list, char="#"):
    """returns list with elements without char"""
    s = []
    for line in list:
        if char not in line:
            s.append(line)
    return s


def myformat(table):
    """creates str from table and formats it"""
    m = 0
    table = sorted(table, key=itemgetter(0))
    for t in table:
        t = str(t)
        if len(t[0]) > m:
            m = len(t[0])
    m += 10
    fstr = "{0:}" + m*" " + "{1:}"
    s = ""
    for x in table:
        try:
            a = float(x[0])
            b = float(x[1])
            s += "{0:.5f}{1:{width}}".format(a, b, width=m) + "\n"
        except IndexError:
            pass
    return s
    """
    out = ""
    for pair in table:
        out += str(pair[0]) + 5*" " + str(pair[1]) + "\n"
    return out"""


def average(data_list):
    return sum(data_list) / len(data_list)


if __name__ == "__main__":
    pass
