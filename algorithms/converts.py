from tkinter import Tk, Button, TOP
from common import myformat, clear_list


class Convert(object):

    def __init__(self, textfield):
        self.textField = textfield
        self.txt = self.textField.get_text()
        self.root = Tk()
        self.root.title("Convert")
        self.root.geometry("150x150")
        self.B1, self.B2, self.B3, self.B4 = None, None, None, None
        self._create()

    def _create(self):
        self.B1 = Button(self.root, text="From hipparcos", command=self._do_bhip)
        self.B1.pack(side=TOP)
        self.B2 = Button(self.root, text="From Integral", command=self._do_bint)
        self.B2.pack(side=TOP)
        self.B3 = Button(self.root, text="From nsvs", command=self._do_bnsvs)
        self.B3.pack(side=TOP)

    def _do_bhip(self):
        self.textField.clear()
        self.textField.insert_text(hipparcos(self.txt))
        self.root.destroy()

    def _do_bint(self):
        self.textField.clear()
        self.textField.insert_text(integral(self.txt))
        self.root.destroy()

    def _do_bnsvs(self):
        self.textField.clear()
        self.textField.insert_text(nsvs(self.txt))
        self.root.destroy()

def hipparcos(text):
    CONST = 2440000
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("|")
    try:
        for line in text:
            s = float(line[0])
            x = []
            x.append(str(s + CONST))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def integral(text):
    CONST = 2451544.5
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split(" ")
    for el in text:
        el = clear_list(el)
    print(text)
    try:
        for line in text:
            x = []
            s = float(line[0])
            x.append(str(s + CONST))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def nsvs(text):
    CONST = 2450000.5
    a = []
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("\t")
    try:
        for line in text:
            x = []
            s = float(line[0])
            x.append(str(s + CONST))
            x.append(str(round(float(line[1]), 3)))
            a.append(x)
    except (IndexError, ValueError):
        pass
    return myformat(a)


def asas(text):
    print(text)