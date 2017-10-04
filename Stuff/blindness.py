#! python3


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep

import random
import os.path
import os

from common import ExperimentFrame, InstructionsFrame
from gui import GUI



sintro = """Nyní následuje druhá část studie.

Budeme Vám znovu prezentovat všechny popisy z předchozí části. Uvidíte také, zda jste popsané chování hodnotili jako morálně špatné nebo nikoliv.
Vaším úkolem bude označit, zda bylo Vaše hodnocení založeno na intuici nebo naopak spíše na rozumové úvaze.

Svou volbu můžete upravovat, ale jakmile kliknete na tlačítko Pokračovat, přesunete se na novou obrazovku s popisem následujícího chování.

(Pokud budete chtít po druhém přečtení své hodnocení popsaného chování změnit, můžete tak učinit zaškrtnutím příslušného políčka.)
"""

tintro = """\n\n\n
Nyní se Vás ještě zeptáme na několik otázek týkajících se průběhu studie a požádáme Vás o uvedení demografických údajů.
"""



delibtext = "Označte na škále, nakolik bylo Vaše původní hodnocení chování intuitivní nebo racionální."
changetext = "Pokud chcete po druhém přečtení popisu chování změnit své původní hodnocení, zaškrtněte toto políčko:"



n_items = 8
n_manipulated = 2


behavioral = []
with open("behavioral.txt") as f:
    for line in f:
        behavioral.append(line.strip())

evaluative = []
with open("evaluative.txt") as f:
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

        self.nchar = 75
        self.count = 0
        self.root = root
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.up = Canvas(self, background = "white", width = 40, height = 50,
                         highlightbackground = "white", highlightcolor = "white")
        self.up.grid(row = 0, column = 0, sticky = S)
        self.upfiller = Canvas(self.up, background = "white", width = 1, height = 70,
                             highlightbackground = "white", highlightcolor = "white")
        self.upfiller.grid(row = 0, column = 1, rowspan = 2)
        
        self.text = Text(self, font = "helvetica 20", relief = "flat", background = "white",
                         width = self.nchar - 8, height = 5, cursor = "arrow",
                         selectbackground = "white", selectforeground = "black")
        self.text.grid(row = 1, column = 0, padx = 2, sticky = S)

        self.questions = Canvas(self, background = "white", width = 40, height = 300,
                                highlightbackground = "white", highlightcolor = "white")
        self.questions.grid(row = 2, column = 0)
        self.filler = Canvas(self.questions, background = "white", width = 1, height = 250,
                             highlightbackground = "white", highlightcolor = "white")
        self.filler.grid(column = 2, row = 1, rowspan = 4)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 1)


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
        self.file.write(self.trialText + "\t" + answer + "\t" + rt + "\n")
        self.count += 1
        if self.count == n_items:
            self.nextFun()
            return
        self.erase()

        self.displayAnswer()
        self.run()


    def erase(self):
        if type(self) is Second:
            for child in self.questions.winfo_children():
                child.grid_remove()
                self.filler.grid(column = 2, row = 0, rowspan = 4)
            for child in self.up.winfo_children():
                child.grid_remove()
                self.upfiller.grid(row = 0, column = 1, rowspan = 2)
        else:
            self.yes["state"] = "disabled"
            self.no["state"] = "disabled"

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
        ttk.Style().configure("TButton", font = "helvetica 15")

        qtext = "Je dle Vás popsané chování morálně špatné?"
        self.question = ttk.Label(self.questions, text = qtext, background = "white",
                                  font = "helvetica 17")
        self.question.grid(row = 0, column = 0, columnspan = 2, pady = 15)

        self.yes = ttk.Button(self.questions, text = "Ano", command = lambda: self.proceed("yes"))
        self.yes.grid(row = 1, column = 0)
   
        self.no = ttk.Button(self.questions, text = "Ne", command = lambda: self.proceed("no"))
        self.no.grid(row = 1, column = 1)

        self.yes["state"] = "disabled"
        self.no["state"] = "disabled"

    def displayQuestions(self):
        self.yes["state"] = "!disabled"
        self.no["state"] = "!disabled"
        
    def displayAnswer(self):
        pass





        
class Second(Situations):
    def __init__(self, root):
        super().__init__(root)

        self.questions.root = self
        ttk.Style().configure("TCheckbutton", font = "helvetica 15", background = "white")

        self.group = random.choice(["present", "absent"])
        self.file.write("group\t{}\n\n".format(self.group))

        if self.group == "present":
            self.displayAnswer()

    def displayQuestions(self):
        self.changeVar = StringVar()
        self.changeVar.set("0")
        
        if self.group == "absent":
            self.displayAnswer()

        self.changeText = ttk.Label(self.questions, text = changetext)
        self.changeText.grid(row = 1, column = 0, pady = 30)
        
        self.change = ttk.Checkbutton(self.questions, variable = self.changeVar, text = "")
        self.change.grid(row = 1, column = 1, padx = 5)

        self.slider = SliderFrame(self.questions, delibtext)
        self.slider.grid(row = 2, column = 0, columnspan = 2)

        self.next = ttk.Button(self.questions, text = "Pokračovat", command = self.proc)
        self.next.grid(row = 3, column = 0, pady = 30, columnspan = 2)
        self.next["state"] = "disabled"

    def rated(self):
        self.next["state"] = "!disabled"

    def proc(self):
        man = "M" if situations[self.count][0] in manipulated else "o"
        ans = "{}\t{}\t{}".format(man, self.changeVar.get(), self.slider.slider.var.get())
        self.proceed(ans)

    def displayAnswer(self):
        prevtext = "Bylo podle Vás popsané chování morálně špatné:"
        ans = self.root.answers[situations[self.count][0]] == "yes" # comment out for testing
        #ans = True # for testing
        ans = not ans if situations[self.count][0] in manipulated else ans
        answer = "ANO" if ans else "NE"
        self.previous = ttk.Label(self.up, text = prevtext, background = "white",
                                  font = "helvetica 17")
        self.previous.grid(row = 0, column = 0, sticky = S, columnspan = 2)
        self.prevans = ttk.Label(self.up, text = answer, background = "white",
                                  font = "helvetica 20 bold")
        self.prevans.grid(row = 1, column = 0, sticky = S, columnspan = 2, pady = 5)        

        self.update()
        sleep(1)


class SliderFrame(Canvas):
    def __init__(self, root, text):
        super().__init__(root)
        
        self.root = root 
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TLabel", background = "white", font = "helvetica 15")

        self.low = ttk.Label(self, text = "intuitivní", width = 10, anchor = "e")
        self.high = ttk.Label(self, text = "racionální", width = 10, anchor = "w")
        self.text = ttk.Label(self, text = text, width = 81, anchor = "center")
        
        self.slider = Slider(self)
        
        self.text.grid(column = 1, row = 0, pady = 5, columnspan = 3)
        self.low.grid(column = 1, row = 1)
        self.slider.grid(column = 2, row = 1, padx = 10)
        self.high.grid(column = 3, row = 1)



class Slider(ttk.Scale):
    def __init__(self, root):
        self.var = StringVar()
        self.var.set("50")
        ttk.Style().configure("TScale", background = "white")
        super().__init__(root, orient = HORIZONTAL, from_ = 0, to = 100, variable = self.var,
                         command = self.move, length = 600)
        self.root = root
        
    def move(self, _):
        self.root.root.root.rated()
        



class DebriefingOne(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\n")

        q1 = ("Pokud se Vám zdá, že jste měl(a) potíže s pochopením instrukcí či jejich "
              "plněním nebo jste během experimentu nebyl(a) plně soustředěn(á), "
              "pravděpodobně bychom neměli použít Vaše data.\n"
              "Myslíte si, že bychom měli použít Vaše odpovědi?")
        q2 = "Všiml(a) jste si něčeho neočekávaného během experimentu?"

        self.question1 = Question(self, q1, label = False)
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
        self.question1.write()
        self.question2.write()

    def rated(self):
        pass


        
class Question(Canvas):
    def __init__(self, root, text, conditional = None, condtype = None, condtext = "", width = 80,
                 label = True, answer = "yesno", condition = "yes"):
        super().__init__(root)
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        self.root = root

        self.yesno = answer == "yesno"
        self.condition = condition

        self.answer = StringVar()
        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 13")

        if label:
            self.label = ttk.Label(self, text = text, background = "white", font = "helvetica 15",
                                   width = width)
        else:
            self.label = Text(self, width = width, wrap = "word", font = "helvetica 15",
                              relief = "flat", height = 5, cursor = "arrow",
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
        q2 = ("Při druhém zobrazení situací Vám byla zobrazena Vaše původní odpověď "
              "na otázku, zda je popsané chování morálně špatné. Ve skutečnosti 5 z 40 těchto "
              "odpovědí bylo obráceno. Tj. pokud jste například původně odpověděli Ano, bylo Vám "
              "napsáno, že jste odpověděli Ne. Všiml(a) jste si této záměny?")
        q3 = "Znal(a) jste design/cíl této studie? (např. protože Vám o něm řekli předchozí účastníci)"
             
        self.question1 = Question(self, q1, (ttk.Entry, {"width": 100}), width = 90,
                                  condtype = "entry", condtext = q1a)
        self.question2 = Question(self, q2, label = False)
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
        self.can2 = Canvas(self,background = "white", highlightbackground = "white", height = 190,
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
                self.question3.write()
                self.nextFun()
                return
            elif self.num == 2:
                self.question3.grid(row = 3, column = 1, sticky = "w")
                self.question2.disable()
                self.question2.write()
            elif self.num == 1:
                self.question2.grid(row = 2, column = 1, sticky = "w")
                self.question1.disable()
                self.question1.write()
            self.num += 1
            self.warning.config(foreground = "white")
        else:
            self.back()                    

      





def main():
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([First#,
         #(InstructionsFrame, {"text": sintro}),
         #Second,
         #(InstructionsFrame, {"text": tintro}),
         #DebriefingOne,
         #DebriefingTwo
         ])


if __name__ == "__main__":
    main()

