from tkinter import Toplevel, Button, TOP
from common import myformat, clear_list, get_without
from threading import Thread
from time import time

# TODO
# Add custom converts. User have to specify which columns he wants to convert and CONST to add.


class Convert(Toplevel):

    def __init__(self, textfield, data):
        Toplevel.__init__(self, data)
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
        self.B6 = Button(self, text="From kepler", command=self._do_kepler)
        self.B6.pack(side=TOP)
        self.B7 = Button(self, text="From unknown", command=self._do_unknown)
        self.B7.pack(side=TOP)

    def _do_unknown(self):
        self.textField.clear()
        self.textField.insert_text(unknown(self.txt))
        self.destroy()

    def _do_kepler(self):
        def _worker(textfield, data):
            t1 = time()
            data = kepler(data)
            print("Kepler convertion took: %s" % (time()-t1))
            textfield.clear()
            textfield.insert_text(data)
        self.textField.clear()
        self.textField.insert_text("CALCULATING, PLEASE WAIT!")
        Thread(target=_worker, args=(self.textField, self.txt)).start()
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
    TO_DEL = (29,99, 99,99)
    const = 2450000
    s = get_without(text.split("\n"))
    for x in range(len(s)):
        s[x-1] = s[x-1].split(" ")
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
            x = float(s[0])+const
            # converting float to string, because we need string for myformat()
            x = str(x)
            if x in TO_DEL:
                continue
            out.append((x, p2[min(p2.keys())]))
        except IndexError:
            pass
    out2 = []
    for line in out:
        if '29.999' in line or '99.999' in line:
            continue
        out2.append(line)
    return myformat(out2)


def munipac(text):
    to_del = ("9.9999", "99.9999")
    text = text.split("\n")
    for x in range(len(text)):
        text[x-1] = text[x-1].split(" ")
    del text[0]
    del text[0]
    for y in range(len(text)):
        try:
            for x in range(len(text[y-1])):
                if text[y-1][x-1] in to_del:
                    del text[y-1]
                    break
        except IndexError:
            pass
    for el in text:
        while len(el) > 2:
            del el[2]
    return myformat(clear_list(text))


def unknown(text):
    out = []
    TO_ADD = 2400000.5
    text = text.split("\n")
    del text[0]
    del text[-1]
    for line in text:
        line = line.split(",")
        mjd = float(line[-2]) + TO_ADD
        mag = line[1]
        mjd = str(mjd)
        out.append((mjd, mag))
    return myformat(clear_list(out))


def kepler(text):
    to_add = "24"
    out = []
    text = text.split("\n")
    """text=n.loadtxt("")
    time=text[:,0]
    dtr=text[:,-2]"""
    del text[0]
    del text[-1]
    for line in text:
        line = line.split("\t")
        data = float(line[-2]) * (-1)
        out.append((to_add + line[0], data))
    return myformat(clear_list(out))


def kepler2(text):
    from numpy import array
    from numpy import delete, append
    # to_add = "24"
    data = array(text.split("\n"))
    data = delete(data, (0, len(data)-1))
    out = array([])
    for row in data:
        row = row.split("\t")
        # print(row[0], row[-2])
        out = append(out, (row[0], row[-2]))
    print(out)
