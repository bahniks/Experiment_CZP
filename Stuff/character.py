#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Question, Measure
from gui import GUI
from common import read_all


###########
n_items = 4 
###########

repeated_green = read_all("repeated_green.txt").split("\n")
repeated_filler = read_all("repeated_filler.txt").split("\n")
onetime_green = read_all("onetime_green.txt").split("\n")
onetime_filler = read_all("onetime_filler.txt").split("\n")
immoral = read_all("immoral.txt").split("\n")
names = read_all("names.txt").split("\n")

random.shuffle(repeated_green)
random.shuffle(repeated_filler)
random.shuffle(onetime_green)
random.shuffle(onetime_filler)
random.shuffle(immoral)
random.shuffle(names)

conditions = ["ff", "fg", "gg", "gf"]*(n_items//4)
random.shuffle(conditions)

texts = []
for i in range(n_items):
    text = repeated_filler.pop()
    text += "\n"
    if conditions[i][0] == "f":
        text += repeated_filler.pop()
    else:
        text += repeated_green.pop()
    text += "\n"
    if conditions[i][1] == "f":
        text += onetime_filler.pop()
    else:
        text += onetime_green.pop()
    text += "\n"
    text += immoral.pop()
    text = text.replace("AAA", names.pop())
    texts.append(text)


class Character(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Character\n")

        self.text = Text(self, font = "helvetica 14", relief = "flat", background = "white",
                         width = 80, height = 10, pady = 7, wrap = "word")
        self.text.grid(row = 1, column = 1, columnspan = 3)
        
        q1 = "Jak moc bylo podle Vašeho názoru chování morální nebo nemorální."
        self.measure1 = Measure(self, q1, range(1,7), "Velmi nemorální", "Velmi morální",
                                function = self.enable, questionPosition = "above",
                                labelPosition = "next")
        self.measure1.grid(row = 2, column = 1, columnspan = 3)

        q2 = "Jak je podle Vás AAA celkově morální nebo nemorální?"
        self.measure2 = Measure(self, q2, range(1,7), "Velmi nemorální", "Velmi morální",
                                function = self.enable, questionPosition = "above",
                                labelPosition = "next")
        self.measure2.grid(row = 3, column = 1, columnspan = 3)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.answered, state = "disabled")
        self.next.grid(row = 4, column = 2)

        self.columnconfigure(0, weight = 3)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 3)

        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.order = -1
        self.proceed()
        
    def proceed(self):
        self.order += 1
        if self.order == n_items-1:
            self.nextFun()
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0", "end")
            self.text.insert("end", texts[self.order])
            self.text["state"] = "disabled"
            self.measure1.answer.set("")
            self.measure2.answer.set("")
            self.t0 = perf_counter()

    def enable(self):
        if self.measure1.answer.get() and self.measure2.answer.get():
            self.next["state"] = "!disabled"

    def answered(self):
        self.file.write("\t".join([self.id, self.measure1.answer.get(),
                                   self.measure2.answer.get(),
                                   str(perf_counter() - self.t0)]) + "\n")
        self.proceed()



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Character])
