from tkinter import Menu
from common import Info


class HelpMenu(Menu):

    def __init__(self, data):
        self.master = data
        Menu.__init__(self, self.master, tearoff=0)
        self._create()
        self._create_commands()

    def _create(self):
        self.master.add_cascade(label="Help", menu=self)

    def _create_commands(self):
        self.add_command(label="Help", command=Info.notimplemented)
        self.add_command(label="Licence", command=Info.notimplemented)
        self.add_command(label="About", command=Info.notimplemented)


class EditMenu(Menu):

    def __init__(self, data, textfield):
        self.master = data
        self.textField = textfield
        Menu.__init__(self, self.master, tearoff=0)
        self._create()
        self._create_commands()

    def _create(self):
        self.master.add_cascade(label="Edit", menu=self)

    def _create_commands(self):
        self.add_command(label="Convert", command=self.textField.convert)
        self.add_command(label="Clear", command=self.textField.clear)
        self.add_command(label="Options", command=Info.notimplemented)


class FileMenu(Menu):

    def __init__(self, data, root, textfield):
        self.master = data
        self.textField = textfield
        Menu.__init__(self, self.master, tearoff=0)
        self._create()
        self._create_commands(root)

    def _create(self):
        self.master.add_cascade(label="File", menu=self)

    def _create_commands(self, root):
        self.add_command(label="Load file", command=self.textField.load)
        self.add_command(label="Save file as...", command=self.textField.save)
        self.add_separator()
        self.add_command(label="Quit", command=root.destroy)