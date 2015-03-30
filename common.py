import tkinter.messagebox, tkinter.filedialog
import astropy.io.fits as fits


class Info():

    @staticmethod
    def notimplemented():
        tkinter.messagebox.showinfo("Not implemented", "Not implemented yet")

    @staticmethod
    def about():
        tkinter.messagebox.showinfo("About", __info__)

    @staticmethod
    def askyesno(tit, tex):
        return tkinter.messagebox.askyesno(tit, tex)

    @staticmethod
    def license():
        pass

    @staticmethod
    def license():
        pass

def loadfile():
    x = tkinter.filedialog.askopenfilename()
    if not x:
        return
    x = open(x)
    y = x.read()
    x.close()
    return y
    """
    x = fits.open(x)
    print(x.info())
    return"""


def savefile(text):
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
        if len(list[x-1]) == 0:
            del list[x-1]
    return list


def del_empty_space(list):
    """deletes empty elements with "space" in it"""
    for x in range(len(list)):
        if " " in list[x-1]:
            del list[x-1]
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


def myformat(table):
    m = 0
    for t in table:
        if len(t[0]) > m:
            m = len(t[0])
    m += 5
    fstr = "{0:"+str(m)+"}{1:"+str(m)+"}"
    s = ""
    for x in table:
        s += fstr.format(x[0], x[1]) + "\n"
    return s