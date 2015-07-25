from tkinter import Toplevel, Entry, Label, Button

from algorithms.period import Period


def calculate_period(master, period):
    p = Period(master.unselected_points[0], master.unselected_points[1],
               period=period)
    p = p.calculate()
    master.unselected_points = [[], []]
    for point in p:
        master.unselected_points[0].append(point.jd)
        master.unselected_points[1].append(point.magnitudo)
    master.redraw()


class PeriodBox(object):
    def __init__(self, master, title, message):
        self.master = master
        self.root = Toplevel(self.master.master)
        self.root.title(title)
        Label(self.root, text=message).pack()
        self.entry = Entry(self.root)
        self.entry.pack()
        b = Button(self.root, text="OK",
                   command=self.quit)
        b.pack()
        # self.root.mainloop()

    def quit(self):
        calculate_period(self.master, float(self.entry.get()))
        self.root.destroy()


if __name__ == "__main__":
    s = ["hi"]
    PeriodBox(s, "Period", "Enter period:")
    print(s[0])
