import tkinter.messagebox, tkinter.filedialog


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
    def license():
        pass


def loadfile():
    """loads file. Has build-in file format recognize system
    returns tuple(directory, text)"""
    x = tkinter.filedialog.askopenfilename()
    if not x:
        return
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
    for t in table:
        if len(t[0]) > m:
            m = len(t[0])
    m += 5
    fstr = "{0:"+str(m)+"}{1:"+str(m)+"}"
    s = ""
    for x in table:
        try:
            s += fstr.format(x[0], x[1]) + "\n"
        except IndexError:
            pass
    return s

if __name__ == "__main__":
    pass