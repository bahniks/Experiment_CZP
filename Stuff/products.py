#! python3

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep,  perf_counter
from itertools import chain

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
# CATEGORIES #
##############



##################################################################################################################
# SETTINGS #
############

# format of names of picture files, e.g. ["s", "T"] corresponds to files named: s1.gif, s2.gif ..., T1.gif ...
#categories = ["s", "t"]


##################################################################################################################


files = os.listdir(os.path.join(os.path.dirname(__file__), "Products"))
n_items = int(len(files)/2)
#categoryOneItems = [file for file in files if categories[0] in file]
#categoryTwoItems = [file for file in files if categories[1] in file]

#positions = random.sample([0,1], 2)



class Choices(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Products\n")
        
        files = os.listdir(os.path.join(os.path.dirname(__file__), "Products"))
        products = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]

        with open(os.path.join(os.path.dirname(__file__), "Products", "products.txt")) as f:
            self.pairs = [(count, *line.strip().split("\t")) for count, line in enumerate(f, 1) if
                          count in products]

        random.shuffle(self.pairs)
        self.root.pairs = self.pairs
        
        self.root.selected = []
        self.selected = self.root.selected

        self.order = -1                      

        text = questionText
        self.text = ttk.Label(self, font = "helvetica 16", justify = "center",
                              background = "white", text = text)
        self.text.grid(row = 0, column = 0, sticky = S, pady = 35)
             
        self.twoProducts = TwoProducts(self, oneLabel = True)

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
             



class TwoProducts(Canvas):
    def __init__(self, root, clickable = True, oneLabel = False, small = False):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white",
                         background = "white")

        self.root = root
        self.selected = self.root.selected
        self.small = "_small" if small else ""
            
        if small:
            self["cursor"] = "hand2"
            self.bind("<1>", self.smallclicked)

        padx = 0 if small else 40
        self.leftProduct = OneProduct(self, clickable = clickable,
                                      oneLabel = oneLabel, small = small)
        self.leftProduct.grid(column = 1, row = 1, padx = padx)

        self.rightProduct = OneProduct(self, clickable = clickable,
                                       oneLabel = oneLabel, small = small)
        self.rightProduct.grid(column = 3, row = 1, padx = padx)
                            
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)

    def proceed(self):
        self.root.proceed()

    def changeImages(self, number, label1 = "", label2 = ""):
        if random.randint(0,1) == 1:
            self.leftProduct.changeImage("{}_1{}.gif".format(number, self.small), label1)
            self.rightProduct.changeImage("{}_2{}.gif".format(number, self.small), label2)
        else:
            self.leftProduct.changeImage("{}_2{}.gif".format(number, self.small), label2)
            self.rightProduct.changeImage("{}_1{}.gif".format(number, self.small), label1)

    def smallclicked(self, _):      
        self.root.clicked()



class OneProduct(Canvas):
    def __init__(self, root, clickable = False, oneLabel = False, small = False):
        super().__init__(root, highlightbackground = "white", highlightcolor = "white")

        self["background"] = "white"

        self.root = root
        self.selected = self.root.selected

        if small:
            self.bind("<1>", self.smallclicked)

        self.product = Product(self, clickable = clickable, small = small)
        self.product.grid(column = 1, row = 0)

        self.oneLabel = oneLabel
        #if not oneLabel:
        self.label = ttk.Label(self, text = "", background = "white", font = "helvetica 15")
        self.label.grid(column = 1, row = 1, pady = 8)
        self.bottomLabel = ttk.Label(self, text = "", background = "white",
                                     font = "helvetica 13")
        self.bottomLabel.grid(column = 1, row = 2, pady = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def changeImage(self, file, text = ""):
        if not self.oneLabel:
            self.product.changeImage(file[0])
        else:
            self.product.changeImage(file)
            self.label["text"] = text
            description = ""
            filename = os.path.join(os.path.dirname(__file__), "Products", file)
            with open(filename.replace(".gif", ".txt").replace("small", "")) as f:
                for line in f:
                    description += line
            self.bottomLabel["text"] = description
            
    def proceed(self):
        self.root.proceed()

    def highlight(self):
        self.product.highlight()

    def removeHighlight(self):
        self.product.removeHighlight()

    def smallclicked(self, _):
        self.root.smallclicked(None)


class Product(Label):
    def __init__(self, root, clickable = False, small = False):
        super().__init__(root, background = "white", foreground = "white", relief = "flat",
                         borderwidth = 10)

        if small:
            self["borderwidth"] = 2
            self.bind("<1>", self.smallclicked)

        self.root = root
        self.selected = self.root.selected

        if clickable:
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
        self.selected.append(name)
        self.root.root.root.file.write("\t".join([self.root.root.root.id,
                                                  str(self.root.root.root.order + 1),
                                                  self.root.label["text"],
                                                  str(self.root.root.root.current[0]),
                                                  self.root.root.leftProduct.label["text"],
                                                  self.root.root.rightProduct.label["text"],
                                                  str(time())]
                                                 ) + "\n")
        self.root.proceed()

    def smallclicked(self, _):
        self.root.smallclicked(None)

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

