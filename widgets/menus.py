from tkinter import Menu


class HelpMenu(Menu):

    def __init__(self, master):
        self.master = master
        Menu.__init__(self, self.master, tearoff=0)
        self.create()
        self.create_commands()

    def create(self):
        self.master.add_cascade(label="Help", menu=self)

    def create_commands(self):
        self.add_command(label="Help")
        self.add_command(label="About")


class EditMenu(Menu):

    def __init__(self, master, textfield):
        self.master = master
        self.textField = textfield
        Menu.__init__(self, self.master, tearoff=0)
        self.create()
        self.create_commands()

    def create(self):
        self.master.add_cascade(label="Edit", menu=self)

    def create_commands(self):
        self.add_command(label="Convert", command=self.textField.convert)
        self.add_command(label="Clear", command=self.textField.clear)
        self.add_command(label="Options")


class FileMenu(Menu):

    def __init__(self, master, root, textfield):
        self.master = master
        self.textField = textfield
        Menu.__init__(self, self.master, tearoff=0)
        self.create()
        self.create_commands(root)

    def create(self):
        self.master.add_cascade(label="File", menu=self)

    def create_commands(self, root):
        self.add_command(label="Load file", command=self.textField.load)
        self.add_command(label="Save file as...", command=self.textField.save)
        self.add_separator()
        self.add_command(label="Quit", command=root.destroy)