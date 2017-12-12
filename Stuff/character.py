#! python3
from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os
import re

from common import ExperimentFrame, InstructionsFrame, Question, Measure
from gui import GUI
from common import read_all


intro = """
Následující úkol se týká usuzování o druhých lidech.
Postupně Vám popíšeme osm lidí. U každého člověka Vám ukážeme čtyři výroky, které o něm řekli jeho blízcí. Jedná se o výroky týkající se jeho aktivit, zvyků, ale i obyčejných zážitků a všedních činností. Následně vám popíšeme určitou situaci. Po vás budeme chtít, abyste na základě těchto informací zhodnotil(a) tohoto člověka a situaci, v níž se ocitl.
"""


intro2 = """
Nyní budete číst znovu informace o popsaných osmi lidech. Tentokrát nás však bude zajímat, jaký si myslíte, že má popsaný člověk postoj k ochraně životního prostředí.
"""

CharacterIntro =(InstructionsFrame, {"text": intro, "height": 6})
CharacterIntro2 =(InstructionsFrame, {"text": intro2, "height": 6})


###########
n_items = 8 
###########

repeated_green = read_all("repeated_green.txt").split("\n")
repeated_filler = read_all("repeated_filler.txt").split("\n")
onetime_green = read_all("onetime_green.txt").split("\n")
onetime_filler = read_all("onetime_filler.txt").split("\n")
immoral = read_all("immoral.txt").split("\n")
immoral_short = read_all("immoral_short.txt").split("\n")
names = read_all("names.txt").split("\n")

immoral_random = [i for i in range(len(immoral))]
green_random = [i for i in range(len(onetime_green))]
random.shuffle(immoral_random)
random.shuffle(green_random)

random.shuffle(repeated_filler)
random.shuffle(onetime_filler)
immoral = [immoral[i] for i in immoral_random]
immoral_short = [immoral_short[i] for i in immoral_random]
random.shuffle(names)

conditions = ["ff", "fg", "gg", "gf"]*(n_items//4)
random.shuffle(conditions)

texts = []
for i in range(n_items):
    text = []
    text.append(repeated_filler.pop()) 
    if conditions[i][0] == "f":
        text.append(repeated_filler.pop()) 
    else:
        text.append(repeated_green[green_random.pop()]) 
    text.append(onetime_filler.pop()) 
    if conditions[i][1] == "f":
        text.append(onetime_filler.pop())
    else:
        text.append(onetime_green[green_random.pop()])
    text = ['"' + t + '"' for t in text]
    random.shuffle(text)
    text = "\n\n".join(text)
    text += "\n\n\n"
    text += "Co se stalo:\n"
    text += '"' + immoral[i] + '"'
    text = text.replace("AAA", names[i])
    texts.append(text)


answers = ["Velmi nemorální", "Celkem nemorální", "Spíše nemorální",
           "Spíše morální", "Celkem morální", "Velmi morální"]
answers2 = ["Silně negativní", "Středně negativní", "Spíše negativní",
            "Spíše pozitivní", "Středně pozitivní", "Silně pozitivní"]


class CharacterCommon(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.nameVar = StringVar()

        self.name = ttk.Label(self, font = "helvetica 14 bold", textvariable = self.nameVar,
                              anchor = "center", background = "white")
        self.name.grid(row = 0, column = 2, pady = 15, sticky = S)
        
        self.text = Text(self, font = "helvetica 14", relief = "flat", background = "white",
                         width = 80, height = 20, pady = 7, wrap = "word")
        self.text.grid(row = 1, column = 1, columnspan = 3)
        self.text.tag_configure("bold", font = "helvetica 14 bold")
        
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
        self.initializeQuestions()
        self.proceed()
                 
    def proceed(self):
        self.order += 1
        if self.order == n_items:
            self.nextFun()
        else:
            self.text["state"] = "normal"
            self.text.delete("1.0", "end")
            self.text.insert("end", texts[self.order])
            i_index = self.text.search("Co se stalo:", "1.0")
            self.text.tag_add("bold", i_index, i_index + "+12c")
            self.text["state"] = "disabled"
            self.nameVar.set(names[self.order])
            self.newItem()
            self.t0 = perf_counter()



class Character(CharacterCommon):
    def __init__(self, root):
        super().__init__(root)
        self.file.write("Character\n")

    def initializeQuestions(self):
        self.q1 = "Jak je podle Vašeho názoru morální to, že "
        self.measure1 = Measure(self, self.q1, answers, "", "",
                                function = self.enable, questionPosition = "above")
        self.measure1.grid(row = 2, column = 1, columnspan = 3, pady = 10)

        self.q2 = "Jak je podle Vás AAA celkově morální nebo nemorální?"
        self.measure2 = Measure(self, self.q2, answers, "", "",
                                function = self.enable, questionPosition = "above")
        self.measure2.grid(row = 3, column = 1, columnspan = 3)

    def answered(self):
        self.file.write("\t".join([self.id, self.measure1.answer.get(),
                                   self.measure2.answer.get(), conditions[self.order],
                                   "\t".join(re.findall(r'"(.*?)"', texts[self.order])),
                                   str(perf_counter() - self.t0)]) + "\n")
        self.proceed()
        
    def enable(self):
        if self.measure1.answer.get() and self.measure2.answer.get():
            self.next["state"] = "!disabled"

    def newItem(self):
        self.measure1.answer.set("")
        self.measure2.answer.set("")        
        self.measure1.question["text"] = self.q1 + immoral_short[self.order].replace("AAA", names[self.order])
        self.measure2.question["text"] = self.q2.replace("AAA", names[self.order])
        


class GreenEvaluation(CharacterCommon):
    def __init__(self, root):
        super().__init__(root)
        self.file.write("Green evaluation\n")

    def initializeQuestions(self):
        self.q1 = "Zkuste prosím odhadnout s využitím následující škály, jaký postoj má AAA k ochraně životního prostředí."
        self.measure1 = Measure(self, self.q1, answers2, "", "",
                                function = self.enable, questionPosition = "above")
        self.measure1.grid(row = 2, column = 1, columnspan = 3, pady = 10)

    def answered(self):
        self.file.write("\t".join([self.id, self.measure1.answer.get(), conditions[self.order],
                                   "\t".join(re.findall(r'"(.*?)"', texts[self.order])),
                                   str(perf_counter() - self.t0)]) + "\n")
        self.proceed()        

    def enable(self):
        if self.measure1.answer.get():
            self.next["state"] = "!disabled"

    def newItem(self):
        self.measure1.answer.set("")    
        self.measure1.question["text"] = self.q1.replace("AAA", names[self.order])



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([CharacterIntro,
         Character,
         CharacterIntro2,
         GreenEvaluation
         ])
