#! python3
from tkinter import *
from tkinter import ttk

import os

from common import ExperimentFrame
from gui import GUI


class Demographics(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
       
        self.sex = StringVar()
        self.language = StringVar()
        self.age = StringVar()
        self.hand = StringVar()
        self.student = StringVar()
        self.field = StringVar()
        self.field.set("Nestuduji VŠ")
        self.education = StringVar()

        self.lab1 = ttk.Label(self, text = "Pohlaví:", background = "white",
                              font = "helvetica 15")
        self.lab1.grid(column = 1, row = 1, pady = 2, sticky = W, padx = 2)
        self.lab2 = ttk.Label(self, text = "Věk:", background = "white",
                              font = "helvetica 15")
        self.lab2.grid(column = 1, row = 2, pady = 2, sticky = W, padx = 2)        
        self.lab3 = ttk.Label(self, text = "Mateřský jazyk:  ", background = "white",
                              font = "helvetica 15")
        self.lab3.grid(column = 1, row = 3, pady = 2, sticky = W, padx = 2)
        self.lab4 = ttk.Label(self, text = "Dominantní ruka:  ", background = "white",
                              font = "helvetica 15")
        self.lab4.grid(column = 1, row = 4, pady = 2, sticky = W, padx = 2)
        self.lab5 = ttk.Label(self, text = "Studujete VŠ?  ", background = "white",
                              font = "helvetica 15")
        self.lab5.grid(column = 1, row = 5, pady = 2, sticky = W, padx = 2)
        self.lab6 = ttk.Label(self, text = "Pokud ano, jaký obor? ", background = "white",
                              font = "helvetica 15")
        self.lab6.grid(column = 1, row = 6, pady = 2, sticky = W, padx = 2)
        self.lab7 = ttk.Label(self, text = "Jaké je vaše nejvyšší dosažené vzdělání? ", background = "white",
                              font = "helvetica 15")
        self.lab7.grid(column = 1, row = 7, pady = 2, sticky = W, padx = 2)
        
        self.male = ttk.Radiobutton(self, text = "muž", variable = self.sex, value = "male",
                                    command = self.checkAllFilled)
        self.female = ttk.Radiobutton(self, text = "žena", variable = self.sex,
                                      value = "female", command = self.checkAllFilled)

        self.czech = ttk.Radiobutton(self, text = "český", variable = self.language,
                                     value = "czech", command = self.checkAllFilled)
        self.slovak = ttk.Radiobutton(self, text = "slovenský", variable = self.language,
                                     value = "slovak", command = self.checkAllFilled)
        self.other = ttk.Radiobutton(self, text = "jiný", variable = self.language,
                                     value = "other", command = self.checkAllFilled)

        self.right = ttk.Radiobutton(self, text = "pravá", variable = self.hand,
                                     value = "right", command = self.checkAllFilled)
        self.left = ttk.Radiobutton(self, text = "levá", variable = self.hand,
                                    value = "left", command = self.checkAllFilled)

        self.yes = ttk.Radiobutton(self, text = "ano", variable = self.student,
                                     value = "student", command = self.checkAllFilled)
        self.no = ttk.Radiobutton(self, text = "ne", variable = self.student,
                                    value = "nostudent", command = self.checkAllFilled)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.ageCB = ttk.Combobox(self, textvariable = self.age, width = 6, font = "helvetica 14",
                                  state = "readonly")
        self.ageCB["values"] = tuple([""] + [str(i) for i in range(18, 80)])
        self.ageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.fieldCB = ttk.Combobox(self, textvariable = self.field, width = 15,
                                    font = "helvetica 14", state = "readonly")
        self.fieldCB["values"] = ["Nestuduji VŠ",
                                  "Ekonomie / management",
                                  "Jazyky / mezinárodní studia",
                                  "Kultura / umění",
                                  "Medicína / farmacie",
                                  "Právo / veřejná správa",
                                  "Přírodní vědy",
                                  "Technika / informatika",
                                  "Učitelství / sport",
                                  "Zemědělství / veterina",
                                  "Humanitní / společenské vědy",
                                  "Jiné"]
        self.fieldCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.educationCB = ttk.Combobox(self, textvariable = self.education, width = 22,
                                    font = "helvetica 14", state = "readonly")
        self.educationCB["values"] = ["Základní",
                                      "Středoškolské bez maturity",
                                      "Středoškolské s maturitou",
                                      "Vysokoškolské"]
        self.educationCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())
        

        self.male.grid(column = 2, row = 1, pady = 7, padx = 7, sticky = W)
        self.female.grid(column = 3, row = 1, pady = 7, padx = 7, sticky = W)
        self.czech.grid(column = 2, row = 3, pady = 7, padx = 7, sticky = W)
        self.slovak.grid(column = 3, row = 3, pady = 7, padx = 7, sticky = W)
        self.other.grid(column = 4, row = 3, pady = 7, padx = 45, sticky = W)
        self.ageCB.grid(column = 2, row = 2, pady = 7, padx = 7, sticky = W)
        self.left.grid(column = 2, row = 4, pady = 7, padx = 7, sticky = W)
        self.right.grid(column = 3, row = 4, pady = 7, padx = 7, sticky = W)
        self.yes.grid(column = 2, row = 5, pady = 7, padx = 7, sticky = W)
        self.no.grid(column = 3, row = 5, pady = 7, padx = 7, sticky = W)
        self.fieldCB.grid(column = 2, columnspan = 2, row = 6, pady = 7, padx = 7, sticky = W)
        self.educationCB.grid(column = 2, columnspan = 3, row = 7, pady = 7, padx = 7, sticky = W)

        self.columnconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(9, weight = 1)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 8, column = 2, pady = 15)


    def checkAllFilled(self, _ = None):
        if all([v.get() for v in [self.language, self.age, self.sex,
                                  self.hand, self.field, self.student, self.education]]):
            self.next["state"] = "!disabled"

    def write(self):
        self.file.write("Demographics\n")
        self.file.write("\t".join([self.id, self.sex.get(), self.age.get(), self.language.get(),
                                   self.hand.get(), self.student.get(), self.field.get(),
                                   self.education.get()]) + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Demographics])
