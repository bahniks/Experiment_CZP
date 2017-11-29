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

introtext = """Nyní budete používat tlačítka "E" a "I" na klávesnici k tomu, abyste co nejrychleji roztřídili položky do skupin.
Celkem jsou čtyři skupiny a v každé skupině jsou buď slova nebo obrázky, jak to ukazuje následující tabulka."""
introtext2 = "Úloha má sedm částí. Dávejte pozor! Instrukce se liší u každé části."

introTextIAT1 = """
Používejte prst levé ruky na klávese E pro zaznamenání položky, která náleží do kategorie {}.
Používejte prst pravé ruky na klávese I pro zaznamenání položky, která náleží do kategorie {}.
{}
Pokud uděláte chybu, objeví se červené X. Abyste mohl(a) pokračovat, musíte zmáčknout druhou klávesu.
Odpovídejte co nejrychleji, ale přesně.
"""

byone = "Položky se budou objevovat po jedné.\n"

introTextIAT2 = """{}
Používejte klávesu E pro {} a {}.
Používejte klávesu I pro {} a {}.
Každá položka náleží pouze do jedné kategorie.
{}
Odpovídejte co nejrychleji, ale přesně.
"""

mistake = "\nPokud uděláte chybu, objeví se červené X.\nAbyste mohl(a) pokračovat, musíte zmáčknout druhou klávesu."
same = "\nTato část je stejná jako předchozí část."

introTextIAT3 = """
{}
Používejte prst levé ruky na klávese E pro kategorii {}.
Používejte prst pravé ruky na klávese I pro kategorii {}.

Odpovídejte co nejrychleji, ale přesně.
"""

positionchange = "Pozor, označení skupin má nyní prohozenou stranu!"


##################################################################################################################
# CATEGORIES #
##############

good_words = ["Přitažlivý", "Láska", "Radostný", "Smích", "Usměvavý",
              "Přítel", "Milý", "Nadšený", "Potěšení", "Báječný"]
bad_words = ["Prohnilý", "Nenávist", "Ponížit", "Strašlivý", "Sobecký",
             "Negativní", "Otravný", "Katastrofa", "Bolest", "Ošklivý"]

categoriesNames = ["Dobrý", "Špatný", "Automobil", "Hromadná doprava"]

##################################################################################################################
# SETTINGS #
############

# format of names of picture files, e.g. ["s", "T"] corresponds to files named: s1.gif, s2.gif ..., T1.gif ...
categories = ["a", "m"]

itemsInRound = [20, 20, 20, 40, 40, 20, 40]

##################################################################################################################


all_files = os.listdir(os.path.join(os.path.dirname(__file__), "IAT"))
small_files = [file for file in all_files if "small" in file]
files = [file for file in all_files if "small" not in file]
n_items = int(len(files)/2)
good_words = good_words[:n_items]
bad_words = bad_words[:n_items]
categoryOneItems = [file for file in files if file.startswith(categories[0])]
categoryTwoItems = [file for file in files if file.startswith(categories[1])]
imageType = categoryOneItems[0][-4:]

positions = random.sample([2,3], 2)
rounds = ((positions[0], positions[1]), (1,0), [[positions[0], 1], [positions[1], 0]],
          [[positions[0], 1], [positions[1], 0]], (positions[1], positions[0]),
          [[positions[1], 1], [positions[0], 0]], [[positions[1], 1], [positions[0], 0]])

introTexts = [introTextIAT1.format(categoriesNames[rounds[0][0]], categoriesNames[rounds[0][1]], byone),
              introTextIAT1.format(categoriesNames[rounds[1][0]], categoriesNames[rounds[1][1]], ""),
              introTextIAT2.format("", categoriesNames[rounds[2][0][0]], categoriesNames[rounds[2][0][1]],
                                   categoriesNames[rounds[2][1][0]], categoriesNames[rounds[2][1][1]], mistake),
              introTextIAT2.format(same, categoriesNames[rounds[3][0][0]], categoriesNames[rounds[3][0][1]],
                                   categoriesNames[rounds[3][1][0]], categoriesNames[rounds[3][1][1]], ""),
              introTextIAT3.format(positionchange, categoriesNames[rounds[4][0]],
                                   categoriesNames[rounds[4][1]]),
              introTextIAT2.format("", categoriesNames[rounds[5][0][0]], categoriesNames[rounds[5][0][1]],
                                   categoriesNames[rounds[5][1][0]], categoriesNames[rounds[5][1][1]], mistake),
              introTextIAT2.format(same, categoriesNames[rounds[6][0][0]], categoriesNames[rounds[6][0][1]],
                                   categoriesNames[rounds[6][1][0]], categoriesNames[rounds[6][1][1]], "")
              ]

allItems = [good_words, bad_words, categoryOneItems, categoryTwoItems]



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
        categoriesFrames = []
        categoriesContent = []
        categoriesTexts = ["Položky", ", ".join(good_words), ", ".join(bad_words),
                           categoryOneItems, categoryTwoItems]
        self.images = []
        for row in range(0, 5):
            # left column
            labelFrames.append(ttk.Frame(self.categories))
            labelFrames[row].grid(row = row, column = 0, sticky = "NSEW")
            labelFrames[row].columnconfigure(0, weight = 1)
            labelFrames[row].rowconfigure(0, weight = 1)
            bckg = "grey90" if row == 0 else "white"
            labels.append(ttk.Label(labelFrames[row], text = labelsTexts[row] + " "*5, font = "Helvetica 15",
                                    background = bckg))
            labels[row].grid(row = 0, column = 0, sticky = "NSEW", padx = 2, pady = 1)
            # right column
            categoriesFrames.append(ttk.Frame(self.categories))
            categoriesFrames[row].grid(row = row, column = 1, sticky = EW)
            categoriesFrames[row].columnconfigure(0, weight = 1)
            if type(categoriesTexts[row]) == list:
                content = Canvas(categoriesFrames[row], background = bckg)
                pictures = []
                for col, file in enumerate(categoriesTexts[row]):
                    img = PhotoImage(file = os.path.join(os.path.dirname(__file__), "IAT",
                                                         file.replace(".ppm", "_small.ppm")))
                    self.images.append(img)
                    pictures.append(ttk.Label(content))
                    pictures[col]["image"] = img
                    pictures[col].grid(row = 0, column = col)
            else:
                content = ttk.Label(categoriesFrames[row], text = categoriesTexts[row], font = "Helvetica 15",
                                    background = bckg)
            categoriesContent.append(content)
            categoriesContent[row].grid(row = 0, column = 0, sticky = NSEW, padx = 1, pady = 1)



class CommonFrame(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.indices = rounds[self.root.IATround]
        if type(self.indices) == list:
            self.labelLeft = categoriesNames[rounds[self.root.IATround][0][1]]
            self.labelRight = categoriesNames[rounds[self.root.IATround][1][1]]
            self.labelLeft2 = categoriesNames[rounds[self.root.IATround][0][0]]
            self.labelRight2 = categoriesNames[rounds[self.root.IATround][1][0]]
            self.categoryLeft2 = ttk.Label(self, text = self.labelLeft2, font = "helvetica 22",
                                          background = "white", foreground = "green")
            self.categoryLeft2.grid(row = 4, column = 1, sticky = "N")        
            self.categoryRight2 = ttk.Label(self, text = self.labelRight2, font = "helvetica 22",
                                          background = "white", foreground = "green")
            self.categoryRight2.grid(row = 4, column = 3, sticky= "N")
            self.orLeft = ttk.Label(self, text = "nebo", font = "helvetica 18", background = "white")
            self.orLeft.grid(row = 3, column = 1, pady = 5)        
            self.orRight = ttk.Label(self, text = "nebo", font = "helvetica 18", background = "white")
            self.orRight.grid(row = 3, column = 3, pady = 5)
        else:
            self.labelLeft = categoriesNames[rounds[self.root.IATround][0]]
            self.labelRight = categoriesNames[rounds[self.root.IATround][1]]
        self.color = "green" if self.labelLeft in categoriesNames[2:4] else "blue"
        self.categoryLeft = ttk.Label(self, text = self.labelLeft, font = "helvetica 22", anchor = "center",
                                      background = "white", foreground = self.color, width = 20)
        self.categoryLeft.grid(row = 2, column = 1)        
        self.categoryRight = ttk.Label(self, text = self.labelRight, font = "helvetica 22", anchor = "center",
                                      background = "white", foreground = self.color, width = 20)
        self.categoryRight.grid(row = 2, column = 3)

        self.textLeft = ttk.Label(self, text = 'Zmáčkněte "E" pro' , font = "courier 11", background = "white")
        self.textLeft.grid(row = 1, column = 1, pady = 5)        
        self.textRight = ttk.Label(self, text = 'Zmáčkněte "I" pro' , font = "courier 11", background = "white")
        self.textRight.grid(row = 1, column = 3, pady = 5)

        self.mainText = Text(self, width = 75, height = 10, relief = "flat", background = "white",
                     highlightbackground = "white", font = "helvetica 20", wrap = "word")
        self.finishText()
        x_index = self.mainText.search("X", "1.0")
        if x_index:
            self.mainText.tag_add("red", x_index, x_index + "+1c")
            self.mainText.tag_configure("red", font = "helvetica 20 bold", foreground = "red")    
        self.mainText.config(state = "disabled")
        self.mainText.grid(row = 6, column = 1, columnspan = 3)

        self.finishInitialization()
        


class Instructions(CommonFrame):
    def __init__(self, root):
        self.root = root
        if hasattr(self.root, "IATround"):
            self.root.IATround += 1
        else:
            self.root.IATround = 0
        super().__init__(root)

    def finishInitialization(self):
        self.partText = ttk.Label(self, text = "Část {} z 7".format(self.root.IATround + 1), background = "white",
                                  font = "helvetica 20 underline")
        self.partText.grid(row = 5, column = 2)

        self.spaceBarText = Text(self, width = 60, height = 1, relief = "flat", background = "white",
                                 highlightbackground = "white", font = "helvetica 20")
        self.spaceBarText.insert("1.0", "Zmáčkněte ")
        self.spaceBarText.insert("end", "mezerník", "bold")
        self.spaceBarText.insert("end", " jakmile budete připraveni začít.")
        self.spaceBarText.tag_configure("bold", font = "helvetica 20 bold")
        self.spaceBarText.tag_add("center", "1.0", "end")
        self.spaceBarText.tag_configure("center", justify = 'center')
        self.spaceBarText.config(state = "disabled")
        self.spaceBarText.grid(row = 7, column = 1, columnspan = 3)
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(6, weight = 1)
        self.rowconfigure(8, weight = 3)

        self.root.bind("<space>", lambda e: self.nextFun())


    def finishText(self):
        self.mainText.insert("1.0", introTexts[self.root.IATround])
        category1_index = self.mainText.search(self.labelLeft, "1.0")
        self.mainText.tag_add("self.colored", category1_index,
                              category1_index + "+{}c".format(len(self.labelLeft)))
        category2_index = self.mainText.search(self.labelRight, "1.0")
        self.mainText.tag_add("self.colored", category2_index,
                              category2_index + "+{}c".format(len(self.labelRight)))
        self.mainText.tag_configure("self.colored", foreground = self.color)
        if type(self.indices) == list:
            category3_index = self.mainText.search(self.labelLeft2, "1.0")
            self.mainText.tag_add("green", category3_index,
                                  category3_index + "+{}c".format(len(self.labelLeft2)))
            category4_index = self.mainText.search(self.labelRight2, "1.0")
            self.mainText.tag_add("green", category4_index,
                                  category4_index + "+{}c".format(len(self.labelRight2)))
            self.mainText.tag_configure("green", foreground = "green")  
        e_index = self.mainText.search("E", "1.0")
        i_index = self.mainText.search("I", "1.0")
        self.mainText.tag_add("bold", e_index, e_index + "+1c")
        self.mainText.tag_add("bold", i_index, i_index + "+1c")
        change_index = self.mainText.search(positionchange, "1.0")
        if change_index:
            self.mainText.tag_add("bold", change_index, change_index + "+{}c".format(len(positionchange)))
        self.mainText.tag_configure("bold", font = "helvetica 20 bold")
        fastText = "co nejrychleji"
        fast_index = self.mainText.search(fastText, "1.0")
        self.mainText.tag_add("underline", fast_index, fast_index + "+{}c".format(len(fastText)))
        self.mainText.tag_configure("underline", font = "helvetica 20 underline")


    def nextFun(self):
        self.root.unbind("<space>")
        super().nextFun()


    
class IAT(CommonFrame):
    def __init__(self, root):
##        self.root = root #
##        if hasattr(self.root, "IATround"): #
##            self.root.IATround += 1 #
##        else: #
##            self.root.IATround = 3 #
        root.file.write("IAT" + str(root.IATround + 1) + "\n")
        super().__init__(root)

    def finishInitialization(self):
        self.textVar = StringVar()
        self.itemLab = ttk.Label(self, textvariable = self.textVar, font = "helvetica 40", background = "white")
        self.itemLab.grid(row = 4, column = 2)

        self.mainText.tag_configure("red", font = "helvetica 15 bold") 

        self.filler = Canvas(self, background = "white", width = 1, height = 250,
                             highlightbackground = "white", highlightcolor = "white")
        self.filler.grid(row = 4, column = 0)
        self.filler2 = Canvas(self, background = "white", width = 400, height = 1,
                             highlightbackground = "white", highlightcolor = "white")
        self.filler2.grid(row = 5, column = 2, sticky = N)

        self.mistakeLab = ttk.Label(self, text = '' , font = "arial 30 bold", background = "white",
                                    foreground = "red")
        self.mistakeLab.grid(row = 5, column = 1, columnspan = 3)
        
        self.columnconfigure(0, weight = 2)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(4, weight = 2)
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(8, weight = 3)

        self.categoriesIndices = rounds[self.root.IATround]
        if type(self.categoriesIndices) == list:
            self.categoriesIndices = list(chain.from_iterable(self.categoriesIndices))
        self.items = []
        itemsPerCategory = int(itemsInRound[self.root.IATround] / len(self.categoriesIndices))
        for i in self.categoriesIndices:
            categoryItems = allItems[i]
            self.items += categoryItems * (itemsPerCategory // n_items)
            self.items += random.sample(categoryItems, itemsPerCategory % n_items)
        random.shuffle(self.items)
        self.trial = -1
        
    def finishText(self):
        self.mainText.insert("1.0", mistake)
        self.mainText["height"] = 3
        self.mainText["font"] = "helvetica 15"
        
    def mistake(self):
        self.mistakeLab["text"] = "X"

    def run(self):
        sleep(0.25)
        self.showItem()

    def showItem(self):
        self.trial += 1
        if self.trial == itemsInRound[self.root.IATround]:
            self.nextFun()
            return
        self.item = self.items[self.trial]
        if self.item.endswith(imageType):
            self.image = PhotoImage(file = os.path.join(os.path.dirname(__file__), "IAT", self.item))
            self.itemLab["image"] = self.image
        else:
            self.textVar.set(self.item)
        self.update()
        self.bindKeys()
        self.t0 = perf_counter()

    def answered(self, answer, t1):
        self.unbindKeys()
        results = [self.id, self.root.IATround + 1, self.trial+1, self.item, answer, t1-self.t0, self.labelLeft,
                   self.labelRight]
        if len(self.categoriesIndices) == 4:
            results += [self.labelLeft2, self.labelRight2]
        if self.item.endswith(imageType):
            correct = categoriesNames[2] if self.item in categoryOneItems else categoriesNames[3]
        else:
            correct = categoriesNames[0] if self.item in good_words else categoriesNames[1]
        if not answer == correct:
            self.mistake()
            self.bindKeys()
            self.file.write("\t".join(map(str, results)) + "\tincorrect" + "\n")
            return
        self.file.write("\t".join(map(str, results)) + "\tcorrect" + "\n")
        self.mistakeLab["text"] = ""
        self.itemLab["image"] = ""
        self.textVar.set("")
        self.update()
        sleep(0.25)
        self.showItem()
        self.update()

    def unbindKeys(self):
        self.root.unbind("<e>")
        self.root.unbind("<E>")
        self.root.unbind("<i>")
        self.root.unbind("<I>")        

    def bindKeys(self):
        self.root.bind("<e>", self.leftPressed)
        self.root.bind("<E>", self.leftPressed)
        self.root.bind("<i>", self.rightPressed)
        self.root.bind("<I>", self.rightPressed)

    def leftPressed(self, e):
        t1 = perf_counter()
        if type(self.indices) == list:
            answer = self.labelLeft2 if self.item.endswith(imageType) else self.labelLeft
        else:
            answer = self.labelLeft 
        self.answered(answer, t1)

    def rightPressed(self, e):
        t1 = perf_counter()
        if type(self.indices) == list:
            answer = self.labelRight2 if self.item.endswith(imageType) else self.labelRight
        else:
            answer = self.labelRight
        self.answered(answer, t1)
        


def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Introduction,
         Instructions,
         IAT,
         Instructions,
         IAT,
         Instructions,
         IAT,
         Instructions,
         IAT,
         Instructions,
         IAT,
         Instructions,
         IAT,
         Instructions,
         IAT
         ])


if __name__ == "__main__":
    main()

