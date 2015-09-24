from tkinter import Toplevel, Button, TOP, Label
import tkinter.filedialog

from common import myformat, clear_list, get_without
from algorithms.tests import perftest


# TODO
# Add custom converts. User have to specify which columns he wants to convert and CONST to add.

class MassConvert(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("MassConvert")
        self.geometry("350x350")
        self.info = Label(self, text="Choose data type, then load your files.\n"
                                     "Converted version will be saved in same directories\n"
                                     "as *.out files. \n"
                                     "kepler data is large, convering one file may take\n"
                                     "few minutes. While converting lots of files, waiting time\n"
                                     "may be over few hours and program WILL NOT respond.\n"
                                     "Please be patient.\n")
        self.info.pack(side=TOP)
        self.B1 = Button(self, text="From hipparcos", command=self._do_bhip)
        self.B1.pack(side=TOP)
        self.B2 = Button(self, text="From Integral", command=self._do_bint)
        self.B2.pack(side=TOP)
        self.B3 = Button(self, text="From nsvs", command=self._do_bnsvs)
        self.B3.pack(side=TOP)
        self.B4 = Button(self, text="From asas", command=self._do_asas)
        self.B4.pack(side=TOP)
        self.B5 = Button(self, text="From munipac", command=self._do_munipac)
        self.B5.pack(side=TOP)
        self.B6 = Button(self, text="From kepler", command=self._do_kepler)
        self.B6.pack(side=TOP)
        self.B7 = Button(self, text="From Catalina", command=self._do_catalina)
        self.B7.pack(side=TOP)

    def get_files(self):
        return tkinter.filedialog.askopenfilenames()

    def handle_convertion(self, file, convert_ref):
        file_ref = file
        file = open(file, "r")
        data = file.read()
        file.close()
        data = convert_ref(data)
        directory = file_ref.split("/")
        del directory[-1]
        directory = "/".join(directory) + "/"
        file_name = file_ref.split("/")
        file_name = file_name[-1]
        file_name = file_name.split(".")
        print(file_name)
        file_name = file_name[0] + ".out"
        print(directory)
        print(file_name)
        file = open(directory + file_name, "w")
        file.write(data)
        file.close()

    def _do_catalina(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, catalina)

    def _do_bhip(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, hipparcos)

    def _do_asas(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, asas)

    def _do_bint(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, integral)

    def _do_bnsvs(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, nsvs)

    def _do_munipac(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, munipac)

    def _do_kepler(self):
        files = self.get_files()
        for file in files:
            self.handle_convertion(file, kepler)


class Convert(Toplevel):
    def __init__(self, textfield, data):
        Toplevel.__init__(self, data)
        self.master = data
        self.textField = textfield
        self.txt = self.textField.get_text()
        self.title("Convert")
        self.geometry("150x200")
        self.master.windows.append(self)
        self.B1, self.B2, self.B3, self.B4, self.B5 = None, None, None, None, None
        self._create()

    def _create(self):
        self.B1 = Button(self, text="From hipparcos", command=self._do_bhip)
        self.B1.pack(side=TOP)
        self.B2 = Button(self, text="From Integral", command=self._do_bint)
        self.B2.pack(side=TOP)
        self.B3 = Button(self, text="From nsvs", command=self._do_bnsvs)
        self.B3.pack(side=TOP)
        self.B4 = Button(self, text="From asas", command=self._do_asas)
        self.B4.pack(side=TOP)
        self.B5 = Button(self, text="From munipac", command=self._do_munipac)
        self.B5.pack(side=TOP)
        self.B6 = Button(self, text="From kepler", command=self._do_kepler)
        self.B6.pack(side=TOP)
        self.B7 = Button(self, text="From Catalina", command=self._do_catalina)
        self.B7.pack(side=TOP)

    def _do_catalina(self):
        self.textField.clear()
        self.textField.insert_text(catalina(self.txt))
        self.destroy()

    def _do_kepler(self):
        self.textField.clear()
        data = kepler(self.textField.directory)
        self.textField.insert_text(data)
        self.destroy()

    def _do_bhip(self):
        self.textField.clear()
        self.textField.insert_text(hipparcos(self.txt))
        self.destroy()

    def _do_bint(self):
        self.textField.clear()
        self.textField.insert_text(integral(self.txt))
        self.destroy()

    def _do_bnsvs(self):
        self.textField.clear()
        self.textField.insert_text(nsvs(self.txt))
        self.destroy()

    def _do_asas(self):
        self.textField.clear()
        self.textField.insert_text(asas(self.txt))
        self.destroy()

    def _do_munipac(self):
        self.textField.clear()
        self.textField.insert_text(munipac(self.txt))
        self.destroy()


def hipparcos(text):
    const = 2440000
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("|")
    try:
        for line in text:
            s = float(line[0])
            x = []
            x.append(str(s + const))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def integral(text):
    const = 2451544.5
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split(" ")
    for el in text:
        clear_list(el)
    try:
        for line in text:
            x = []
            s = float(line[0])
            x.append(str(s + const))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def nsvs(text):
    const = 2450000.5
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("\t")
    try:
        for line in text:
            x = []
            s = float(line[0])
            x.append(str(s + const))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def asas(text):
    to_del = (29, 99, 99, 99)
    const = 2450000
    s = get_without(text.split("\n"))
    for x in range(len(s)):
        s[x - 1] = s[x - 1].split(" ")
    for element in s:
        clear_list(element)
    p = s
    out = []
    for s in p:
        try:
            p2 = {
                s[6]: s[1],
                s[7]: s[2],
                s[8]: s[3],
                s[9]: s[4],
                s[10]: s[5],
            }
            # creating float because we need sum, and can't use int()
            x = float(s[0]) + const
            # converting float to string, because we need string for myformat()
            x = str(x)
            if x in to_del:
                continue
            out.append((x, p2[min(p2.keys())]))
        except IndexError:
            pass
    out2 = []
    for line in out:
        if '29.999' in line or '99.999' in line:
            continue
        out2.append(line)
    return myformat(clear_list(out2))


def munipac(text):
    to_del = ("9.9999", "99.9999")
    text = text.split("\n")
    for x in range(len(text)):
        text[x - 1] = text[x - 1].split(" ")
    del text[0]
    del text[0]
    for y in range(len(text)):
        try:
            for x in range(len(text[y - 1])):
                if text[y - 1][x - 1] in to_del:
                    del text[y - 1]
                    break
        except IndexError:
            pass
    for el in text:
        while len(el) > 2:
            del el[2]
    return myformat(clear_list(text))


def catalina(text):
    out = []
    to_add = 2400000.5
    text = text.split("\n")
    del text[0]
    del text[-1]
    for line in text:
        line = line.split(",")
        mjd = float(line[-2]) + to_add
        mag = line[1]
        mjd = str(mjd)
        out.append((mjd, mag))
    return myformat(clear_list(out))


@perftest
def kepler(path):
    """ this is temporary solution. It will accept path to the file instead of text from textField. Later, during
    changes in load system i'm going to rewrte this function """
    import numpy as np
    data = np.loadtxt(path)
    first = data[:, 0]
    second = data[:, -2]
    out = ""
    if len(first) != len(second):
        return "OOPS, ERROR"
    for i in range(len(first)):
        out += "24" + str(first[i]) + "\t" + str(second[i]) + "\n"
    return out


def kepler2(text):
    from numpy import array
    from numpy import delete, append
    # to_add = "24"
    data = array(text.split("\n"))
    data = delete(data, (0, len(data) - 1))
    out = array([])
    for row in data:
        row = row.split("\t")
        # print(row[0], row[-2])
        out = append(out, (row[0], row[-2]))
    print(out)
