from tkinter import Toplevel, Entry, Label, Button

from algorithms.period import Period
import numpy as np

def calculate_period(master, period, is_phase, mo):

    p = Period(master.unselected_points[0,:].tolist(),
               master.unselected_points[1,:].tolist(),
               mo, is_phase, period=period)
    p = p.calculate()
    master.unselected_points = np.array([[],[]])
    for point in p:
        master.unselected_points = np.hstack((master.unselected_points, [[point.jd],[point.magnitudo]]))
    master.redraw()


class PeriodBox(object):
    def __init__(self, master, title):
        self.master = master
        self.root = Toplevel(self.master.master)
        self.root.title(title)
        Label(self.root, text="M_0: ").pack()
        self.entry1 = Entry(self.root)
        self.entry1.pack()
        self.entry1.insert(0, "2450000")
        Label(self.root, text="period: ").pack()
        self.entry2 = Entry(self.root)
        self.entry2.pack()
        self.entry2.insert(0, "10")
        Button(self.root, text="Phase", command=self.phase).pack()
        Button(self.root, text="JDHel", command=self.jdhel).pack()
        # self.root.mainloop()

    def phase(self):
        self.quit(True)

    def jdhel(self):
        self.quit(False)

    def quit(self, is_phase):
        calculate_period(self.master, float(self.entry2.get()), is_phase, float(self.entry1.get()))
        self.root.destroy()


if __name__ == "__main__":
    s = ["hi"]
    PeriodBox(s, "Period", "Enter period:")
    print(s[0])
