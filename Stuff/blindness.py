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

fintro = read_all("choice_blindness_intro1.txt")
sintro = read_all("choice_blindness_intro2.txt")
tintro = read_all("choice_blindness_intro3.txt")

ChoiceBlindnessInstructions1 = (InstructionsFrame, {"text": fintro, "height": 8})
ChoiceBlindnessInstructions2 = (InstructionsFrame, {"text": sintro, "height": 8})
ChoiceBlindnessInstructions3 = (InstructionsFrame, {"text": tintro, "height": 8})



##################################################################################################################
# TEXTS #
#########

changetext = "(Pokud chcete, můžete své hodnocení ještě změnit. Změnu provedete zakliknutím odpovědi, kterou chcete vybrat.)"

beh_answers = ["Nikdy", "Zřídka", "Občas", "Často", "Velmi často", "Vždy"]
eval_answers = ["Velmi špatná", "Celkem špatná", "Spíše špatná", "Spíše dobrá", "Celkem dobrá", "Velmi dobrá"]

beh_question = "Jak tuto aktivitu často provádíte?"
eval_question = "Jak tuto aktivitu celkově hodnotíte?"

beh_question2 = "Myslíte si, že tuto aktivitu provádíte častěji, než většina lidí v našem vzorku?"
eval_question2 = "Myslíte si, že tuto aktivitu hodnotíte pozitivněji, než většina lidí v našem vzorku?"

beh_statement = "Uvedl(a) jste, že tuto aktivitu provádíte:"
eval_statement = "Uvedl(a) jste, že tuto aktivitu hodnotíte:"

blindnessQuestion = """
V jedné části experimentu jsme Vám ukazovali Vaše původní odpovědi na otázku, jestli určitá chování hodnotíte jako dobré nebo špatné, anebo jak často tato chování vykonáváte. Ve skutečnosti bylo 5 ze 46 těchto odpovědí posunuto o tři body opačným směrem. Tj. pokud jste například původně odpověděl(a) "Celkem špatné", zobrazilo se Vám "Spíše dobré" a pokud jste odpověděl(a) "Zřídka", zobrazilo se Vám "Často". Všiml(a) jste si této záměny?
""" 

##################################################################################################################
# SETTINGS #
############

n_items = 46
n_manipulated = 5

##################################################################################################################



behavioral = []
with open(os.path.join(os.path.dirname(__file__), "behavioral.txt")) as f:
    for line in f:
        behavioral.append(line.strip())

evaluative = []
with open(os.path.join(os.path.dirname(__file__), "evaluative.txt")) as f:
    for line in f:
        evaluative.append(line.strip())

items = random.sample([i for i in range(len(behavioral))], n_items)
eval_behav = ["E"]*int(n_items/2) + ["B"]*int(n_items/2)
random.shuffle(eval_behav)
manipulated = ["M"]*(n_manipulated) + ["n"]*(n_items-n_manipulated)
random.shuffle(manipulated)

trials = [i for i in zip(items, eval_behav, manipulated)]



class Situations(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.nchar = 55
        self.count = 0
        self.root = root
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.up = Canvas(self, background = "white", width = 40, height = 50,
                         highlightbackground = "white", highlightcolor = "white")
        self.up.grid(row = 0, column = 0, sticky = S)
        self.upfiller = Canvas(self.up, background = "white", width = 1, height = 70,
                             highlightbackground = "white", highlightcolor = "white")
        self.upfiller.grid(row = 0, column = 1, rowspan = 2)
        
        self.text = Text(self, font = "helvetica 22", relief = "flat", background = "white",
                         width = self.nchar, height = 4, cursor = "arrow",
                         selectbackground = "white", selectforeground = "black")
        self.text.grid(row = 1, column = 0, padx = 2, sticky = S)

        self.questions = Canvas(self, background = "white", width = 40, height = 300,
                                highlightbackground = "white", highlightcolor = "white")
        self.questions.grid(row = 2, column = 0, sticky = N)
        self.filler = Canvas(self.questions, background = "white", width = 1, height = 250,
                             highlightbackground = "white", highlightcolor = "white")
        self.filler.grid(column = 2, row = 0, rowspan = 4)

        self.downfiller = Canvas(self, background = "white", width = 1, height = 150,
                                 highlightbackground = "white", highlightcolor = "white")
        self.downfiller.grid(column = 2, row = 3, rowspan = 1)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 2)

    def initializeText(self):
        self.content = []
        trial = trials[self.count]
        situations = behavioral if trial[1] == "B" else evaluative
        self.trialText = situations[trial[0]]
        words = self.trialText.split(" ")
        chars = 0
        temp = []
        for word in words:
            chars += len(word)
            if chars > self.nchar:
                self.content.append(temp)
                temp = [word]
                chars = len(word) + 1
            else:
                chars += 1
                temp.append(word)
        else:
            self.content.append(temp)

        self.content = [" ".join(line) for line in self.content]
        
    def run(self):
        self.config(cursor = "none")
        self.text.config(state = "normal")
        self.initializeText()
        self.text.delete("1.0", "end")
        t = time()
        line = 0
        char = 0
        allchars = 0
        letter = 0.065 # 0.065 seconds per letter 
        pause = 0.35 # 0.35 seconds after a line 
        while True:
            self.update()
            curLine = self.content[line]
            if not curLine:
                line += 1
                continue
            if time() > t + allchars*letter + line*pause:
                self.text.insert("end", curLine[char], ("standard"))
                char += 1
                allchars += 1
                if char == len(curLine):
                    line += 1
                    char = 0
                    if line == len(self.content):
                        self.update()
                        break
                    else:
                        self.text.insert("end", "\n")

        self.config(cursor = "")
        self.displayWidgets()
        self.t0 = time()

    def displayWidgets(self):
        self.text.config(state = "disabled")
        self.displayQuestions()

    def proceed(self, answer):
        rt = str(time() - self.t0)
        if type(self) is First:
            self.root.answers[self.trialText] = answer
        results = [self.id, str(self.count + 1), self.trialText, str(trials[self.count][0]),trials[self.count][1],
                   answer.replace(" ", "_"), rt]
        self.file.write("\t".join(results) + "\n")
        self.count += 1
        if self.count == n_items:
            self.nextFun()
            return

        self.erase()
        self.run()

    def erase(self):
        self.eraseWidgets()
        self.config(cursor = "none")
        self.text.config(state = "normal")
        self.initializeText()
        self.text.delete("1.0", "end")
        
        self.update()
        sleep(0.5)
    


class First(Situations):
    def __init__(self, root):
        super().__init__(root)

        self.root.answers = {}
        self.file.write("Choice blindness\n")
 
    def displayQuestions(self):
        qtext = beh_question if trials[self.count][1] == "B" else eval_question
        answers = beh_answers if trials[self.count][1] == "B" else eval_answers
        color = "green" if trials[self.count][1] == "B" else "orange"
        self.measure = Measure(self.questions, qtext, answers, "", "", function = self.answered,
                               questionPosition = "above")
        self.measure.question["font"] = "helvetica 16"
        self.measure.grid(row = 2, column = 0)
        self.measure.question = Text(self.measure, width = len(qtext)-4, height = 1, relief = "flat",
                                     background = "white", highlightbackground = "white", font = "helvetica 18")
        self.measure.question.grid(column = 0, row = 0, columnspan = 4)
        self.measure.question.insert("1.0", qtext)
        index = self.measure.question.search("aktivitu", "1.0")
        self.measure.question.tag_add("color", index + "+9c", "end - 2chars")
        self.measure.question.tag_configure("color", foreground = color, font = "helvetica 18 bold") 

    def answered(self):
        self.proceed(self.measure.answer.get())

    def eraseWidgets(self):
        self.measure.grid_remove()

        
       
class Second(Situations):
    def __init__(self, root):
        super().__init__(root)

        self.rowconfigure(0, weight = 8)
        self.rowconfigure(1, weight = 0)
        self.rowconfigure(2, weight = 4)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 2)

        self.questions.root = self
        self.file.write("Choice blindness second part\n")
        self.filler["height"] = 400

    def displayQuestions(self):
        self.label = ttk.Label(self.questions, text = changetext, background = "white", font = "helvetica 12")
        self.label.grid(row = 2, column = 0, sticky = N, pady = 5)
        
        qtext = beh_statement if trials[self.count][1] == "B" else eval_statement
        answers = beh_answers if trials[self.count][1] == "B" else eval_answers
        self.measure = Measure(self.questions, qtext, answers, "", "", function = self.fakeFunction,
                               questionPosition = "above")
        self.measure.question["font"] = "helvetica 16"
        self.measure.grid(row = 1, column = 0)
        index = answers.index(self.root.answers[self.trialText])
        if trials[self.count][2] == "M":
            index = index - 3 if index > 2 else index + 3
        self.shownAnswer = answers[index]
        self.measure.answer.set(self.shownAnswer)

        qtext2 = beh_question2 if trials[self.count][1] == "B" else eval_question2
        self.measure2 = Measure(self.questions, qtext2, ["Ano", "Ne"], "", "", function = self.rated,
                                questionPosition = "above", filler = 400)
        self.measure2.question["font"] = "helvetica 16"
        self.measure2.grid(row = 3, column = 0, sticky = S)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.proc)
        self.next.grid(row = 3, column = 0, pady = 30, columnspan = 2)
        self.next["state"] = "disabled"

    def fakeFunction(self):
        pass

    def rated(self):
        self.next["state"] = "!disabled"

    def proc(self):
        ans = "{}\t{}\t{}\t{}".format(trials[self.count][2], self.measure.answer.get(),
                                      self.measure2.answer.get(), self.measure.answer.get() == self.shownAnswer)
        self.proceed(ans)

    def eraseWidgets(self):
        for child in self.questions.winfo_children():
            child.grid_remove()
            self.filler.grid(column = 2, row = 0, rowspan = 4)
        for child in self.up.winfo_children():
            child.grid_remove()
            self.upfiller.grid(row = 0, column = 1, rowspan = 2)



       



class DebriefingOne(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        q1 = ("Pokud se Vám zdá, že jste měl(a) potíže s pochopením instrukcí či jejich "
              "plněním nebo jste během experimentu nebyl(a) plně soustředěn(á), "
              "pravděpodobně bychom neměli použít Vaše data.\n"
              "Myslíte si, že bychom měli použít Vaše odpovědi?")
        q2 = "Všiml(a) jste si něčeho neočekávaného během experimentu?"

        self.question1 = Question(self, q1, label = False, lines = 3)
        self.question2 = Question(self, q2, (ttk.Entry, {"width": 100}),
                                  condtype = "entry", condtext = "Čeho jste si všimli?")

        self.question1.grid(row = 1, column = 1, sticky = "w")
        self.question2.grid(row = 2, column = 1, sticky = "w")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 4, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na všechny otázky.",
                                 background = "white", font = "helvetica 15", foreground = "white")
        self.warning.grid(row = 5, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(6, weight = 1)

        self.next.bind("<FocusIn>", lambda e: self.focus_set())
        
    def check(self):
        return self.question1.check() and self.question2.check()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(self.id + "\t")
        self.question1.write(newline = False)
        self.file.write("\t")
        self.question2.write()

    def rated(self):
        pass


       
class Question(Canvas):
    def __init__(self, root, text, conditional = None, condtype = None, condtext = "", width = 80,
                 label = True, answer = "yesno", condition = "yes", lines = 5):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.yesno = answer == "yesno"
        self.condition = condition

        self.answer = StringVar()
        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 14")

        if label:
            self.label = ttk.Label(self, text = text, background = "white", font = "helvetica 15",
                                   width = width)
        else:
            self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                              relief = "flat", height = lines, cursor = "arrow",
                              selectbackground = "white", selectforeground = "black")
            self.label.insert("1.0", text)
            self.label.config(state = "disabled")

        if answer == "yesno":
            self.yes = ttk.Radiobutton(self, text = "Ano", variable = self.answer, value = "yes",
                                       command = self.answered)
            self.no = ttk.Radiobutton(self, text = "Ne", variable = self.answer, value = "no",
                                       command = self.answered)
            self.yes.grid(column = 0, row = 1, sticky = "w", padx = 5)
            self.no.grid(column = 0, row = 2, sticky = "w", padx = 5)
        else:
            self.field = answer[0](self, textvariable = self.answer, **answer[1])
            self.field.grid(column = 0, row = 1, sticky = "w", padx = 5)

        self.condtype = condtype
        if conditional:
            self.condvar = StringVar()
            if condtype in ("combo", "entry"):
                self.cond = conditional[0](self, textvariable = self.condvar, **conditional[1])
            else:
                self.cond = conditional[0](self, variable = self.condvar, **conditional[1])
            if condtype == "combo":
                self.cond.config(state = "readonly")
            self.cond.grid(column = 2, row = 1, sticky = "w")
            self.condtext = ttk.Label(self, text = condtext, background = "white",
                                      font = "helvetica 13")
            self.condtext.grid(column = 1, row = 1, sticky = "w", padx = 20)
            self.condtext.grid_forget()
            self.cond.grid_forget()
                        
        self.label.grid(column = 0, row = 0, columnspan = 4, sticky = "w", pady = 10)

        self.columnconfigure(3, weight = 1)


    def answered(self):
        if self.condtype:
            if self.answer.get() == self.condition:
                row = 1 if self.condition == "yes" else 2
                self.condtext.grid(column = 1, row = row, sticky = "w", padx = 20)
                self.cond.grid(column = 2, row = row, sticky = "w")
            else:
                self.condtext.grid_forget()
                self.cond.grid_forget()

    def check(self):
        return self.answer.get() and (not self.condtype or self.condvar.get()
                                      or self.answer.get() != self.condition)

    def write(self, newline = True):
        self.root.file.write(self.answer.get())
        if self.condtype and self.condvar.get():
            self.root.file.write("\t" + self.condvar.get())
        if newline:
            self.root.file.write("\n")

    def disable(self):
        if self.yesno: 
            self.yes.config(state = "disabled")
            self.no.config(state = "disabled")
        else:
            self.field.config(state = "disabled")
        if self.condtype:
            self.cond.config(state = "disabled")

            


class DebriefingTwo(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file = self.root.file
        self.root = root
        self.file.write("Debriefing2\n")

        self.num = 1

        q1 = 'Víte, co značí termín "choice blindness" neboli "slepota k volbě"?'
        q1a = "Stručně prosím význam popište."
        q2 = blindnessQuestion
        q3 = "Znal(a) jste design/cíl této studie? (např. protože Vám o něm řekli předchozí účastníci)"
             
        self.question1 = Question(self, q1, (ttk.Entry, {"width": 100}), width = 90,
                                  condtype = "entry", condtext = q1a)
        self.question2 = Question(self, q2, label = False, lines = 6)
        self.question3 = Question(self, q3, width = 90)

        self.question1.grid(row = 1, column = 1, sticky = "w")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)
        self.next.grid(row = 5, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na otázku.",
                                 background = "white", font = "helvetica 15", foreground = "white",
                                 width = 100, anchor = "center")
        self.warning.grid(row = 6, column = 1)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 2)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 2)
        self.rowconfigure(7, weight = 1)

        self.can1 = Canvas(self, background = "white", highlightbackground = "white", height = 100,
                           width = 1).grid(row = 1, column = 0, sticky = (N, S))
        self.can2 = Canvas(self,background = "white", highlightbackground = "white", height = 220,
                           width = 1).grid(row = 2, column = 0, sticky = (N, S))
        self.can3 = Canvas(self, background = "white", highlightbackground = "white", height = 100,
                           width = 1).grid(row = 3, column = 0, sticky = (N, S))


        self.next.bind("<FocusIn>", lambda e: self.focus_set())

        
    def check(self):
        checks = sum((1 for i in range(3) if (self.question1.check(),
                                              self.question2.check(),
                                              self.question3.check())[i]))
        return checks == self.num

    def back(self):
        self.warning.config(foreground = "red")
       

    def proceed(self):
        if self.check():
            if self.num == 3:
                self.file.write("\t")
                self.question3.write()
                self.nextFun()
                return
            elif self.num == 2:
                self.question3.grid(row = 3, column = 1, sticky = "w")
                self.question2.disable()
                self.file.write("\t")
                self.question2.write(newline = False)
            elif self.num == 1:
                self.question2.grid(row = 2, column = 1, sticky = "w")
                self.question1.disable()
                self.file.write(self.id)
                self.file.write("\t")
                self.question1.write(newline = False)
            self.num += 1
            self.warning.config(foreground = "white")
        else:
            self.back()                    

      

ChoiceBlindness1 = First
ChoiceBlindness2 = Second



def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([ChoiceBlindnessInstructions1,
         ChoiceBlindness1,
         ChoiceBlindnessInstructions2,
         ChoiceBlindness2,
         ChoiceBlindnessInstructions3,
         DebriefingOne,
         DebriefingTwo
         ])


if __name__ == "__main__":
    main()

