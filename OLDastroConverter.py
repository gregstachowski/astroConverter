"""
************************* INFO ***************************
I know it's only one file, but it's way more comfortable 
for the user.                                            
created by: 											  
konrad.wybraniec@gmail.com                               
**********************************************************
"""
__info__ = """astroConverter v0.2
created by Konrad Wybraniec
"""

# ToDo:
# re-write GUI - it should use classes
# converting and convert options

from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
#from convert import auto_convert

root = Tk()
root.title("astroConverter")
root.geometry("800x600")

# ******** FUNCTIONS ********
#convert hipparcos
def convert_hipparcos(text):
    CONST = 2440000
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("|")
    try:
        for line in text:
            s = float(line[0])
            line[0] = str(s + CONST)
            del line[3]
            del line[2]
            line[1] = str(round(float(line[1]),3))
    except (IndexError, ValueError):
        pass
    s = ""
    for line in text:
        for el in line:
            s += el + "\t\t"
        s += "\n"
    return s

def convert_Integral(text):
    CONST = 2451544.5
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split(" ")
    print(text)
    try:
        for line in text:
            s = float(line[0])
            line[0] = str(s + CONST)
            del line[3]
            line[1] = str(round(float(line[1]),3))
    except (IndexError, ValueError):
        pass
    s = ""
    for line in text:
        for el in line:
            s += el + "\t\t"
        s += "\n"
    return s


def convert_nsvs(text):
    CONST = 2450000.5
    text = text.split("\n")
    for x in range(len(text)):
        text[x] = text[x].split("\t")
    print(text)
    try:
        for line in text:
            s = float(line[0])
            line[0] = str(s + CONST)
            del line[3]
            del line[2]
    except (IndexError, ValueError):
        pass
    s = ""
    for line in text:
        for el in line:
            s += el + "\t\t"
        s += "\n"
    return s


def loadFile():
    if len(textField.get(0.0,END)) > 1:
        s = Info.askYesNo("Are you sure?", "Text field isn't empty. Are you sure you want to load? You will loose your changes!")
        if not s:
            return
    x = tkinter.filedialog.askopenfilename()
    if not x:
        return
    clearTextField()
    textField.insert(0.0, open(x).read())


def saveFile():
    file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if not file: return
    file.write(textField.get(0.0, END))
    file.close()


def clearTxtField():
    if Info.askYesNo("Are you sure?", "Delete text?"):
        clearTextField()


def clearTextField():
    textField.delete(0.0, END)


def convert():
    """if Info.askYesNo("Are you sure?", "Do you want to convert text file? You will loose your changes!"):
        s = auto_convert(textField.get(0.0, END))
        clearTextField()
        textField.insert(0.0, s)"""
    #Info.notImplemented()
    text = textField.get(0.0, END)
    clearTextField()
    textField.insert(0.0, convert_nsvs(text))


#******** CLASSESS ********
class Info():

    def notImplemented():
        tkinter.messagebox.showinfo("Not implemented", "Not implemented yet")

    def about():
        tkinter.messagebox.showinfo("About", __info__)

    def askYesNo(tit, tex):
        return tkinter.messagebox.askyesno(tit, tex)


#******** BUILDING GUI ********
#******** MAIN MENU ********
mainMenu = Menu(root)
root.config(menu=mainMenu)
fileMenu = Menu(mainMenu, tearoff = 0)
helpMenu = Menu(mainMenu, tearoff=0)
editMenu = Menu(mainMenu, tearoff=0)
mainMenu.add_cascade(label="File", menu=fileMenu)
mainMenu.add_cascade(label="Edit", menu=editMenu)
mainMenu.add_cascade(label="Help", menu=helpMenu)

#fileMenu
fileMenu.add_command(label="Load file", command = loadFile)
fileMenu.add_command(label="Save file as ...", command = saveFile)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command = root.destroy)

#editMenu
editMenu.add_command(label="Clear text", command = clearTxtField)
editMenu.add_command(label="Convert", command = convert)
editMenu.add_command(label="Options", command=Info.notImplemented)

#helpMenu
helpMenu.add_command(label="Help", command = Info.notImplemented)
helpMenu.add_command(label="About", command = Info.about)


#******** TOOLBAR ********
toolbar = Frame(root)
lButton = Button(toolbar, text="Load", command = loadFile)
sButton = Button(toolbar, text="Save", command = saveFile)
clearButton = Button(toolbar, text="Clear", command=clearTxtField)
convertButton = Button(toolbar, text="Convert", command = convert)
lButton.pack(side=LEFT)
sButton.pack(side=LEFT)
clearButton.pack(side=LEFT)
convertButton.pack(side=LEFT)
toolbar.pack(side = TOP, fill=X)

#******** CENTER ********
textField = Text(root, width = 50, height = 30, wrap = NONE)
ys = Scrollbar(root, orient = VERTICAL, command = textField.yview) #vertical(y) scrollbarr
ys.pack(side=RIGHT, fill=Y)
xs = Scrollbar(root, orient=HORIZONTAL, command = textField.xview) #horizontal(x) scrollbar
xs.pack(side=BOTTOM, fill=X)
textField['ys']=ys.set
textField['xs']=xs.set
textField.pack(side=LEFT, fill=BOTH, expand=YES)

root.mainloop()
