#! python3
from tkinter import *
from tkinter import ttk

import os
from urllib.request import urlopen

from common import ExperimentFrame
from gui import GUI



instruction = """Do textového pole napište své identifikační číslo.
Pokud budete mít s přihlášením problém, zavolejte experimentátora zvednutím ruky."""


url = "https://osf.io/enqax/download"
site = urlopen(url)
text = site.read()
site.close()
text = str(text, 'utf-8')
codes = [code.rstrip() for code in text.split("\n")]


class Validation(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
       
        self.code = StringVar()

        self.lab = ttk.Label(self, text = instruction, background = "white",
                              font = "helvetica 15")
        self.lab.grid(column = 1, row = 1, columnspan = 3)

        vcmd = (self.register(self.validate), '%P')
        self.entry = ttk.Entry(self, textvariable = self.code, width = 20, font = "helvetica 14",
                               validate = "key", validatecommand = vcmd)
        self.entry.grid(column = 2, row = 2, pady = 20)
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(5, weight = 3)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 2, pady = 15)


    def validate(self, code):
        if code in codes:
            self.next["state"] = "!disabled"
        elif code == "admin":
            self.next["state"] = "!disabled"
        else:
            self.next["state"] = "disabled"
        return True


    def write(self):
        self.file.write("Identificator\n")
        self.file.write(self.id + "\t" + self.code.get() + "\n")




if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Validation])
