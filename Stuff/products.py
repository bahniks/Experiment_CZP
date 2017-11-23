#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep,  perf_counter
from itertools import chain
from collections import defaultdict

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame, read_all, Measure
from gui import GUI



##################################################################################################################
# TEXTS #
#########

#introtext = """Vaším úkolem bude používat klávesy 'E' a 'I' pro co nejrychlejší kategorizaci položek do skupin.
#Toto jsou zmiňované čtyři skupiny a položky, které do nich patří:"""
#introtext2 = "Úloha má sedm částí. Dávejte pozor! Instrukce se liší u každé části."

questionText = """Který z dvojice výrobků byste si raději odnesl(a) domů?
Vyberte kliknutím na obrázek."""

##################################################################################################################



class Choices(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Products\n")
        
        files = os.listdir(os.path.join(os.path.dirname(__file__), "Products"))
        products = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]

        self.pairs = [[("{}_1.gif".format(i), "{}_2.gif".format(i)),
                       ("{}_1.gif".format(i), "{}_3.gif".format(i)),
                       ("{}_2.gif".format(i), "{}_3.gif".format(i))] for i in products]
        self.pairs = list(chain(*self.pairs))
        for i in range(len(self.pairs)):
            if random.randint(0,1) == 1:
                self.pairs[i] = (self.pairs[i][0], self.pairs[i][1])
            else:
                self.pairs[i] = (self.pairs[i][1], self.pairs[i][0])
        random.shuffle(self.pairs)
        self.root.pairs = self.pairs
        
        self.root.selected = defaultdict(list)
        self.selected = self.root.selected

        self.order = -1                      

        text = questionText
        self.text = ttk.Label(self, font = "helvetica 16", justify = "center",
                              background = "white", text = text)
        self.text.grid(row = 0, column = 0, sticky = S, pady = 35)
             
        self.twoProducts = TwoProducts(self)
        self.twoProducts.grid(row = 1, column = 0)

        self.columnconfigure(0, weight = 1)      
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)

        self.proceed()
        

    def proceed(self):
        self.order += 1
        if self.order == len(self.pairs):
            self.nextFun()
        else:
            self.current = self.pairs[self.order]
            self.twoProducts.changeImages(*self.current)
            self.t0 = time()
             


class TwoProducts(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white",
                         background = "white")

        self.root = root
        self.selected = self.root.selected
            
        self.leftProduct = OneProduct(self)
        self.leftProduct.grid(column = 1, row = 1, padx = 40)

        self.rightProduct = OneProduct(self)
        self.rightProduct.grid(column = 3, row = 1, padx = 40)
                            
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)

    def proceed(self):
        self.root.proceed()

    def changeImages(self, left, right):
        self.leftProduct.changeImage(left)
        self.rightProduct.changeImage(right)



class OneProduct(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white")

        self["background"] = "white"

        self.root = root
        self.selected = self.root.selected

        self.product = Product(self)
        self.product.grid(column = 1, row = 0)

        self.label = ttk.Label(self, text = "", background = "white", font = "helvetica 15")
        self.label.grid(column = 1, row = 1, pady = 8)
        self.bottomLabel = ttk.Label(self, text = "", background = "white",
                                     font = "helvetica 13")
        self.bottomLabel.grid(column = 1, row = 2, pady = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def changeImage(self, file):
        self.product.changeImage(file)
        description = ""
        filename = os.path.join(os.path.dirname(__file__), "Products", file)
        with open(filename.replace(".gif", ".txt")) as f:
            for num, line in enumerate(f):
                if num == 0:
                    self.label["text"] = line.strip()
                else:
                    description += line
        self.bottomLabel["text"] = description
            
    def proceed(self):
        self.root.proceed()

    def highlight(self):
        self.product.highlight()

    def removeHighlight(self):
        self.product.removeHighlight()



class Product(Label):
    def __init__(self, root):
        super().__init__(root, background = "white", foreground = "white", relief = "flat",
                         borderwidth = 10)

        self.root = root
        self.selected = self.root.selected

        self.bind("<Enter>", self.entered)
        self.bind("<Leave>", self.left)
        self.bind("<1>", self.clicked)

    def changeImage(self, file):
        file = os.path.join(os.path.dirname(__file__), "Products", file)
        self.image = PhotoImage(file = file)
        self["image"] = self.image
        self.file = file

    def entered(self, _):
        self.config(cursor = "hand2")

    def left(self, _):
        self.config(cursor = "arrow")

    def clicked(self, _):
        name = os.path.basename(self.file)
        self.selected[name.split("_")[0]].append(name.split("_")[1][0])
        self.root.root.root.file.write("\t".join([self.root.root.root.id,
                                                  str(self.root.root.root.order + 1),
                                                  self.root.label["text"],
                                                  str(self.root.root.root.current[0]),
                                                  self.root.root.leftProduct.label["text"],
                                                  self.root.root.rightProduct.label["text"],
                                                  str(time() - self.root.root.root.t0)]
                                                 ) + "\n")
        self.root.proceed()

    def highlight(self):
        self["background"] = "red"

    def removeHighlight(self):
        self["background"] = "white"
        





def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Choices
         ])


if __name__ == "__main__":
    main()

