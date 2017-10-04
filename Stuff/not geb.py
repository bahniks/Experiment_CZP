from tkinter import *
from tkinter import ttk
from collections import deque
from time import perf_counter, sleep

import random
import os

from common import ExperimentFrame, InstructionsFrame, Question, Measure
from gui import GUI


class GEB(ExperimentFrame):
    def __init__(self, root, words, question = None, ltext = None, rtext = None):
        super().__init__(root)

        self.words = words

        self.buttons = {}
        self.variables = {}
        self.labels = {}

        self.frame = Canvas(self)
        self.frame.grid(column = 1, row = 1, sticky = NSEW)
        self.frame["highlightbackground"] = "white"
        self.frame["background"] = "white"
        self.frame["highlightcolor"] = "white"
        
        for count, word in enumerate(self.words, 1):
            self.variables[word] = StringVar()
            for i in range(1,8):
                if word not in self.buttons:
                    self.buttons[word] = {}
                self.buttons[word][i] = ttk.Radiobutton(self.frame, text = str(i), value = i,
                                                        command = self.clicked,
                                                        variable = self.variables[word])
                self.buttons[word][i].grid(column = i, row = count + (count-1)//5, padx = 15)
            self.labels[word] = ttk.Label(self.frame, text = word, background = "white",
                                          font = "helvetica 12", justify = "left", width = 13)
            self.labels[word].grid(column = 0, row = count + (count-1)//5, padx = 15,
                                   sticky = W)
            if not count % 5:
                self.frame.rowconfigure(count + count//5, weight = 1)
                
        ttk.Label(self.frame, text = " "*60, background = "white", font = "helvetica 3",
                  foreground = "white", justify = "left", width = 60).grid(
                      column = 0, padx = 15, sticky = W, row = count + 1 + (count-1)//5) 
                                   
        if not ltext:
            ltext = "špatně"
        if not rtext:
            rtext = "dobře" 

        self.left = ttk.Label(self.frame, text = ltext, background = "white",
                              font = "helvetica 14")
        self.right = ttk.Label(self.frame, text = rtext, background = "white",
                               font = "helvetica 14")
        self.left.grid(column = 1, row = 0, sticky = W, pady = 4)
        self.right.grid(column = 7, row = 0, sticky = E, pady = 4)
                      
        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 12")

        ttk.Style().configure("TButton", font = "helvetica 15")                
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(column = 1, row = 2)

        if not question:
            question = "Jak vyslovitelná vám přijdou následující slova?"
        self.question = ttk.Label(self, text = question, background = "white",
                                  font = "helvetica 15")
        self.question.grid(column = 1, row = 0)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        

    def clicked(self):
        end = True            
        for word in self.words:
            if not self.variables[word].get():
                end = False
            else:
                self.labels[word]["font"] = "helvetica 10"
        if end:
            self.next["state"] = "!disabled"

    def write(self):
        for word in self.words:
            self.file.write(self.id + "\t" + word + "\t" + self.variables[word].get() + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([(GEB, {"words": ["a"*11 + str(i) for i in range(9)]})])
