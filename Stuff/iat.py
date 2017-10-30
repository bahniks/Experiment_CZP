#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI

#fintro = read_all("iat_intro1.txt")

#IatInstructions1 = (InstructionsFrame, {"text": fintro, "height": 8})




##################################################################################################################
# TEXTS #
#########

introtext = """Vaším úkolem bude používat klávesy 'E' a 'I' pro co nejrychlejší kategorizaci položek do skupin.
Toto jsou zmiňované čtyři skupiny a položky, které do nich patří:"""
introtext2 = "Úloha má sedm částí. Dávejte pozor! Instrukce se liší u každé části." 

good_words = ["Atraktivní", "Láska", "Radostný", "Smích", "Usměvavý", "Přítel", "Milý", "Nadšený"]
bad_words = ["Prohnilý", "Nenávist", "Ponížit", "Strašlivý", "Sobecký", "Negativní", "Otravný", "Katastrofa"]

categoriesNames = ["Dobrý", "Špatný", "Světlý", "Tmavý"]



##################################################################################################################
# SETTINGS #
############

categories = ["s", "t"]

##################################################################################################################


files = os.listdir(os.path.join(os.path.dirname(__file__), "IAT"))
n_items = int(len(files)/2)
good_words = good_words[:n_items]
bad_words = bad_words[:n_items]


##behavioral = []
##with open(os.path.join(os.path.dirname(__file__),"behavioral.txt")) as f:
##    for line in f:
##        behavioral.append(line.strip())
##
##evaluative = []
##with open(os.path.join(os.path.dirname(__file__),"evaluative.txt")) as f:
##    for line in f:
##        evaluative.append(line.strip())
##
##items = random.sample([i for i in range(len(behavioral))], n_items)
##eval_behav = ["E"]*int(n_items/2) + ["B"]*int(n_items/2)
##random.shuffle(eval_behav)
##manipulated = ["M"]*(n_manipulated) + ["n"]*(n_items-n_manipulated)
##random.shuffle(manipulated)
##
##trials = [i for i in zip(items, eval_behav, manipulated)]



class Introduction(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        ttk.Style().configure("TButton", font = "helvetica 15")

        self.labUp = ttk.Label(self, text = introtext, font = "helvetica 20", background = "white")
        self.labUp.grid(row = 1, column = 1)

        self.categories = ttk.Frame(self)
        self.categories.grid(row = 2, column = 1)

        self.labDown = ttk.Label(self, text = introtext2, font = "helvetica 20", background = "white")
        self.labDown.grid(row = 3, column = 1)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 4, column = 1, pady = 30)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        labelFrames = []
        labels = []
        labelsTexts = ["Kategorie"] + categoriesNames
        for row in range(0, 5):
            labelFrames.append(ttk.Frame(self.categories))
            labelFrames[row].grid(row = row, column = 0, sticky = EW)
            labelFrames[row].columnconfigure(0, weight = 1)
            bckg = "grey90" if row == 0 else "white"
            labels.append(ttk.Label(labelFrames[row], text = labelsTexts[row], font = "Helvetica 15",
                                    background = bckg))
            labels[row].grid(row = row, column = 0, sticky = EW, padx = 2, pady = 1)

    def write(self):
        pass



def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Introduction
         ])


if __name__ == "__main__":
    main()

