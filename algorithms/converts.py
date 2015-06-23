from tkinter import Tk, Button, TOP
from common import myformat, clear_list, get_without

# TODO
# Add custom converts. User have to specify which columns he wants to convert and CONST to add.


class Convert(Tk):

    def __init__(self, textfield, data):
        Tk.__init__(self)
        self.master = data
        self.textField = textfield
        self.txt = self.textField.get_text()
        self.title("Convert")
        self.geometry("150x150")
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
    CONST = 2450000
    s = get_without(text.split("\n"))
    for x in range(len(s)):
        s[x-1] = s[x-1].split(" ")
    for el in s:
        el = clear_list(el)
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
            #creating float because we need sum, and can't use int()
            x = float(s[0])+CONST
            #converting float to string, because we need string for myformat()
            x = str(x)
            out.append((x, p2[min(p2.keys())]))
        except IndexError:
            pass
    return myformat(out)


def munipac(text):
    TO_DEL = ("9.9999", "99.9999")
    text = text.split("\n")
    for x in range(len(text)):
        text[x-1] = text[x-1].split(" ")
    del text[0]
    del text[0]
    for y in range(len(text)):
        try:
            for x in range(len(text[y-1])):
                if text[y-1][x-1] in TO_DEL:
                    del text[y-1]
                    break
        except IndexError:
            pass
    for el in text:
        while len(el) > 2:
            del el[2]
    return myformat(clear_list(text))
    