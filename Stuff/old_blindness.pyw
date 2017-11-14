#! python3


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import time, localtime, strftime, sleep, perf_counter

import random
import os.path
import os


intro = """Dobrý den, děkujeme, že se účastníte našeho výzkumu faktorů ovlivňujících spotřebitelské preference.

Nejdříve Vám budeme po dvojicích postupně prezentovat výrobky.
Z každé dvojice si prosím vyberte výrobek, který byste si raději na konci výzkumu odnesl(a) domů.

Jakmile kliknete na obrázek, už svou volbu nemůžete upravovat.

Pro začátek klikněte na tlačítko Pokračovat.
"""


sintro = """\n
Nyní následuje třetí část studie.

Budeme Vám po jednom prezentovat 40 výrobků.
U každého zobrazeného výrobku prosím zvolte, jak moc byste jej chtěli.

Až výrobek ohodnotíte, stiskněte tlačítko Pokračovat.

Svou volbu můžete upravovat, ale jakmile stisknete tlačítko Pokračovat, není možné se vrátit na předchozí obrazovku.
"""

tintro = """\n\n\n\n
Nyní Vám znovu ukážeme výrobek, který jste si zvolil(a).

Uveďte prosím, co se Vám na zvoleném výrobku líbí a vyberte ze seznamu všechny odpovídající důvody, proč jste si z dvojice zvolil(a) právě tento výrobek.
"""



boxt = """\n\n
Čísla krabic uvedené níže si prosím opište do bloku ležícího vedle počítače.

{}

Nyní přejděte ke krabicím a jako odměnu za účast si vyberte jeden výrobek z každé z krabic s čísly, jež jste si opsali.
Vybrané výrobky si prosím vložte do vlastní tašky, případně do tašky, kterou Vám nabídne experimentátor.
Vybrané výrobky jsou Vaše a můžete si je odnést domů.

Až budete mít odměnu vybranou, ohlašte se prosím experimentátorovi.
"""

datestr = strftime("%y_%m_%d", localtime())
files = os.listdir(os.path.join(os.getcwd(), "Data"))
dateord = str(sum([1 for file in files if os.path.basename(file).startswith(datestr)]))
code = datestr.replace("_", "")+ chr(random.randint(65, 90)) + dateord 

codeoutro = 4*"\n" + """\tKód tohoto účastníka je:\n\n\t{}\n\n
\tČísla krabic, ze kterých měl vybírat, jsou:\n\n\t{}""".format(code, "{}")


end = """Děkujeme, že jste se zúčastnil(a) našeho výzkumu. V textu níže máte možnost dozvědět se o něm více.
 
Když si lidé zvolí jednu z dvou možností, předpokládáme, že tím projevili svoji skutečnou preferenci a tudíž, že by si všimli, pokud by místo zvolené věci dostali nakonec tu, již si nevybrali. V nejrůznějších výzkumech se však ukázalo, že tomu tak není. Lidé měli například možnost ochutnat dvě příchutě džemu a vybrat si tu, kterou by si raději odnesli domů. Poté, co si vybrali, dostali svůj džem k ochutnání ještě jednou s dotazem na důvody svého rozhodnutí. Ve skutečnosti však experimentátor šikovným trikem džem vyměnil a lidé ochutnávali druhou, nevybranou příchuť. Překvapivě, ačkoliv příchutě nebyly vůbec podobné, si spousta lidí záměny nevšimla a bez potíží přesvědčivě vysvětlili, jaké důvody je vedly k volbě právě “tohoto” džemu.
Tomuto jevu se říká slepota k volbě (angl. choice blindness) a náš výzkum se ji snažil zkoumat v kontextu výběru potravinových výrobků.
 
K manipulaci došlo v části, kdy jste měli uvádět důvody své volby u dvanácti dvojic produktů - ve 3 náhodně vybraných dvojicích byl jako Vámi vybraný výrobek označen ten, který jste si ve skutečnosti nevybrali. Nás přitom zajímají zejména dvě věci: jestli se nám povede zopakovat výsledky předchozích studií a budeme moct pozorovat fenomén slepoty k volbě i při administraci na počítači. A co víc, zajímá nás také, jaká bude Vaše volba z dvojice skutečných výrobků - zvolíte si spíše ten, který jste si vybrali na začátku, a nebo spíše ten, o kterém jsme Vám tvrdili, že jste jej zvolili a jehož volbu jste měli zdůvodnit.

Fenomén slepoty k volbě se často používá pro podporu hypotézy, že lidé ve skutečnosti nemají fixní preference a proto nemá velký smysl zkoušet tyto preference měřit a zkoumat. Pokud ale prokážeme, že lidé si opravdu z krabice vyberou ten výrobek, který preferovali při první volbě, i když jeho záměnu nezpozorovali, bude to důkaz ve prospěch existenci skutečných preferencí.

Pokud máte nějaké dotazy, neváhejte se s nimi obrátit na administrátora. O výsledcích budete informováni e-mailem a na stránkách www.pless.cz.

Na závěr Vás prosíme, abyste s nikým (zejména s možnými budoucími účastníky) nemluvil(a) o povaze tohoto výzkumu, ani jim neukazoval(a) výrobky, které si odnášíte. Znemožnilo by nám to úspěšné dokončení studie.
"""


def color():
    return "white"

class GUI(Tk):
    def __init__(self):
        super().__init__()

        self.title("Experiment")
        self.config(bg = "white")
        self.state("zoomed")
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        #self.geometry("1366x768")

        self.liking = {}
        
        self.protocol("WM_DELETE_WINDOW", lambda: self.closeFun())
        
        filepath = os.path.join(os.getcwd(), "Data")
        
        writeTime = localtime()
        filename = os.path.join(filepath, strftime("%y_%m_%d_%H%M%S", writeTime) + ".txt")

        self.bind("<Escape>", self.closeFun)


        self.order = [(InstructionsFrame, {"text": intro}),
                      Choices,
                      (InstructionsFrame, {"text": tintro}),
                      Manipulation,
                      (InstructionsFrame, {"text": sintro}),
                      Ratings,
                      BoxInstructions,
                      Demographics,
                      DebriefingOne,
                      DebriefingTwo,
                      Catches,
                      (InstructionsFrame, {"text": end, "proceed": False,
                                           "height": 30, "font": 15}),
                      EndInstructions]
        
        #self.order = [Choices, Manipulation]
                                  
        self.count = -1


        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
                      
        with open(filename, mode = "w") as self.file:
            self.file.write(code + "\n\n")
            self.nextFrame()
            self.mainloop()
        

    def nextFrame(self):
        self.unbind("<g>")                    
        self.count += 1
        if self.count >= len(self.order):
            self.file.write(str(time()))
            self.destroy()
        else:
            nxt = self.order[self.count]
            if isinstance(nxt, tuple):
                self.frame = nxt[0](self, **nxt[1])
            else:
                self.frame = nxt(self)
            self.frame.grid(row = 0, column = 0, sticky = (N, S, E, W))

    def closeFun(self, event = ""):
        message = "Jste si jistí, že chcete studii předčasně ukončit?"
        ans = messagebox.askyesno(message = message, icon = "question", parent = self,
                                  title = "Ukončit studii?")
        if ans:
            self.file.write("\nEnded before the end by Escape.")
            self.destroy()

        

class ExperimentFrame(Canvas):
    def __init__(self, root):
        super().__init__(root)
        
        self.root = root
        self.file = self.root.file    
        self["background"] = "white"

    def nextFun(self):
        if self.check():
            self.write()
            self.file.write("\n")
            self.destroy()
            self.root.nextFrame()
        else:
            self.back()

    def check(self):
        return True

    def back(self):
        pass

    def write(self):
        pass


class InstructionsFrame(ExperimentFrame):
    def __init__(self, root, text, proceed = True, firstLine = None, end = False, height = 12,
                 font = 18):
        super().__init__(root)
        
        self.root = root
        self.t0 = time()
                    
        self.text = Text(self, font = "helvetica {}".format(font), relief = "flat",
                         background = "white", width = 90, height = height, wrap = "word")
        self.text.grid(row = 1, column = 0, columnspan = 3)
        if firstLine:
            self.text.insert("1.0", text[:text.find("\n", 5)], firstLine)
            self.text.insert("end", text[text.find("\n", 5):])
            self.text.tag_configure(firstLine, font = "helvetica 20 {}".format(firstLine))
        else:
            self.text.insert("1.0", text)
        self.text.config(state = "disabled")

        if proceed:
            ttk.Style().configure("TButton", font = "helvetica 15")
            self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
            self.next.grid(row = 2, column = 1)
        else:
            self.root.bind("<g>", lambda e: self.proceed())

        if end:
            self.root.state("normal")
            self.root.attributes("-topmost", False)
            self.root.overrideredirect(False)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 3)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(2, weight = 3)
        self.rowconfigure(3, weight = 3)

    def proceed(self):
        if time() - self.t0 > 2:
            self.nextFun()       



class BoxInstructions(InstructionsFrame):
    def __init__(self, root):
        text = boxt.format("\t".join(map(str, root.boxes)))
        super().__init__(root, text, proceed = False)


class EndInstructions(InstructionsFrame):
    def __init__(self, root):
        text = codeoutro.format("\t".join(map(str, sorted(root.boxes))))
        super().__init__(root, text, proceed = False, end = True, height = 20)



class Ratings(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Ratings\t" + str(time()) + "\n")
        self.products = []
        self.selected = []

        files = os.listdir(os.path.join(os.getcwd(), "Stuff"))
        products = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]

        with open(os.path.join(os.getcwd(), "Stuff", "products.txt")) as f:
            for count, line in enumerate(f, 1):
                if count in products:
                    self.products.extend([("{}_1.gif".format(count), line.strip()),
                                          ("{}_2.gif".format(count), line.strip())])

        random.shuffle(self.products)
        self.order = -1                      

        self.text = ttk.Label(self, font = "helvetica 16", justify = "center",
                              text = "Ohodnoťte prosím tento výrobek.")
        self.text.grid(row = 0, column = 0, sticky = S)
             
        self.product = OneProduct(self, clickable = False)
        self.product.grid(row = 1, column = 0)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)
        self.next.grid(row = 4, column = 0)
        self.next["state"] = "disabled" 

        self.liking = SliderFrame(self, text = "Jak moc byste chtěl(a) tento výrobek?")

        self.like = self.liking.slider

        self.liking.grid(row = 2, column = 0, pady = 10)

        self.columnconfigure(0, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(4, weight = 4)


        self.proceed()


    def proceed(self):
        self.order += 1

        if self.order:
            self.file.write("\t".join([self.products[self.order - 1][0],
                                       str(time()),
                                       self.like.var.get(),
                                       ]) + "\n")
            key = self.products[self.order - 1][0].rstrip(".gif")
            self.root.liking[key] = float(self.like.var.get())
        
        if self.order == len(self.products):
            self.nextFun()
            self.file.write("\n")
        else:
            self.product.changeImage(self.products[self.order])
            self.like.reset()
            self.next["state"] = "disabled"  
            

    def rated(self):
        if self.like.moved:
            self.next["state"] = "!disabled"        



class SliderFrame(Canvas):
    def __init__(self, root, text, left = False):
        super().__init__(root)
        
        self.root = root 
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TLabel", background = "white", font = "helvetica 15")

        if not left:
            self.low = ttk.Label(self, text = "vůbec", width = 6, anchor = "e")
            self.high = ttk.Label(self, text = "hodně", width = 6, anchor = "w")
            self.text = ttk.Label(self, text = text, width = 35, anchor = "center")
        else:
            self.low = ttk.Label(self, text = "Ano", width = 6, anchor = "e")
            self.high = ttk.Label(self, text = "Ne", width = 6, anchor = "w")
            self.text = ttk.Label(self, text = text, width = 50, anchor = "w")
        
        self.slider = Slider(self)
        
        if not left:
            self.text.grid(column = 2, row = 0, pady = 5)
        else:
            self.text.grid(column = 0, row = 0, columnspan = 3, pady = 10, sticky = W)
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
        self.moved = False
        
    def move(self, _):
        self.moved = True
        self.root.root.rated()

    def reset(self):
        self.var.set("50")
        self.moved = False
        




class Choices(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Products\t" + str(time()) + "\n")
        
        files = os.listdir(os.path.join(os.getcwd(), "Stuff"))
        products = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]

        with open(os.path.join(os.getcwd(), "Stuff", "products.txt")) as f:
            self.pairs = [(count, line.strip()) for count, line in enumerate(f, 1) if
                          count in products]

        random.shuffle(self.pairs)
        self.root.pairs = self.pairs
        
        self.root.selected = []
        self.selected = self.root.selected

        self.order = -1                      

        text = ("Který z dvojice výrobků byste si raději odnesl(a) domů? "
                "Vyberte kliknutím na obrázek.")
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
            self.twoProducts.changeImages(*self.pairs[self.order])
             



class Manipulation(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        files = os.listdir(os.path.join(os.getcwd(), "Stuff"))
        files = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]
        products = [file for file in files if file <= 12]

        self.root.boxes = random.sample(products, 6)
        self.root.manipulated = random.sample(self.root.boxes, 3)

        self.file.write("Boxes\t" + "\t".join(map(str, self.root.boxes)) + "\n\n")        

        self.file.write("Reasons\t" + str(time()))
       

        self.pairs = self.root.pairs
        self.selected = self.root.selected

        self.order = -1                      

        text = ("Napište, co se Vám na vybraném výrobku líbí a vyberte důvod(y) proč jste si "
                "vybral(a) právě tento produkt.")
        self.text = ttk.Label(self, font = "helvetica 16", background = "white", text = text,
                              justify = "center")
        self.text.grid(row = 0, column = 0)
             
        self.product = OneProduct(self, clickable = False)

        self.product.grid(row = 1, column = 0)

        self.columnconfigure(0, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(4, weight = 1)


        self.whyvar = StringVar()
        self.whyframe = Canvas(self, background = "white", highlightbackground = "white",
                               highlightcolor = "white")
        self.whyframe.grid(column = 0, row = 2)
        self.whytext = ttk.Label(self.whyframe, text = "Co se Vám líbí na tomto výrobku? ",
                                 font = "helvetica 15", background = "white")
        self.whytext.grid(column = 0, row = 0)
        self.why = ttk.Entry(self.whyframe, textvariable = self.whyvar, width = 70)
        self.why.grid(column = 1, row = 0, padx = 5)

        
        self.reasonsFrame = Canvas(self, background = "white", highlightbackground = "white",
                                   highlightcolor = "white", width = 400, height = 200)
        self.reasonsFrame.grid(row = 3, column = 0)

        ttk.Style().configure("TButton", font = "helvetica 15")

        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)
        self.next.grid(row = 4, column = 0)

        self.reasons = ["Výrobek má hezčí obal",
                        "Výrobek lépe znám",
                        "Mám raději tuto příchuť",
                        "Výrobek má lepší využití",
                        'V tomto výrobku je méně "chemie"',
                        "Výrobek je dražší",
                        "Chtěl(a) jsem zkusit něco nového",
                        "Chtěl(a) jsem tento výrobek někomu darovat",
                        "Jiný důvod",
                        "Vybral(a) bych si jinak / Spletl(a) jsem se"]

        ttk.Style().configure("TCheckbutton", font = "helvetica 15", background = "white")

        for num, reason in enumerate(self.reasons):
            exec("self.var{} = BooleanVar()".format(num))
            exec("""self.chb{} = ttk.Checkbutton(self.reasonsFrame, text = '{}', variable =
                self.var{}, command = self.control)""".format(num, reason, num))
            exec("self.chb{}.grid(row = {}, column = {}, sticky = W, padx = 10)".format(
                num, num // 2, num % 2))

        self.proceed()

    def control(self):
        for num in range(len(self.reasons)):
            if eval("self.var{}.get()".format(num)):
                self.next["state"] = "!disabled"
                break
        else:
            self.next["state"] = "disabled"


    def proceed(self):
        self.next["state"] = "disabled"
        
        if self.order >= 0:
            self.file.write(str(self.pairs[self.order][0]) + "\t" + str(time()))
            if self.pairs[self.order][0] in self.root.manipulated:
                self.file.write("\tM")
            else:
                self.file.write("\tn")
            for num, reason in enumerate(self.reasons):
                if eval("self.var{}.get()".format(num)):
                    self.file.write("\t" + reason)
                exec("self.var{}.set(False)".format(num))
            self.file.write("\t" + self.whyvar.get())
            self.whyvar.set("")

        self.order += 1
        if self.order == len(self.pairs):
            self.nextFun()
        else:
            self.file.write("\n")
            num, label = self.pairs[self.order]
            file = self.selected[self.order]
            
            if num in self.root.manipulated:
                file = "{}_{}.gif".format(num, 3 - int(file.split("_")[1][0]))
            
            self.product.changeImage((file, label))



                    

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

    def changeImages(self, number, label = ""):
        if random.randint(0,1) == 1:
            self.leftProduct.changeImage("{}_1{}.gif".format(number, self.small))
            self.rightProduct.changeImage("{}_2{}.gif".format(number, self.small))
        else:
            self.leftProduct.changeImage("{}_2{}.gif".format(number, self.small))
            self.rightProduct.changeImage("{}_1{}.gif".format(number, self.small))

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
        if not oneLabel:
            self.label = ttk.Label(self, text = "", background = "white", font = "helvetica 15")
            self.label.grid(column = 1, row = 1, pady = 8)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

    def changeImage(self, file):
        if not self.oneLabel:
            self.product.changeImage(file[0])
        else:
            self.product.changeImage(file)
            
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
        file = os.path.join(os.getcwd(), "Stuff", file)
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
        self.root.root.root.file.write("{}\t{}\n".format(name, str(time())))
        self.root.proceed()

    def smallclicked(self, _):
        self.root.smallclicked(None)

    def highlight(self):
        self["background"] = "red"

    def removeHighlight(self):
        self["background"] = "white"
        


class DebriefingOne(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("Debriefing\t{}\n".format(str(time())))

        q1 = "Jste spokojen(a) s výrobky, jež jste si vybral(a) z krabic?"
        q2 = "Napište prosím, co si myslíte, že tento výzkum zkoumal."
        q3 = ("Všimli jste si během výzkumu nějaké chyby nebo nečekaného chování "
              "programu na počítači?")

        self.question1 = SliderFrame(self, text = q1, left = True)
        self.question2 = Question(self, q2, width = 90, answer = (ttk.Entry, {"width": 140}))
        self.question3 = Question(self, q3, (ttk.Entry, {"width": 100}),
                                  condtype = "entry", condtext = "O jakou chybu šlo?")

        self.question1.grid(row = 1, column = 1, sticky = "w")
        self.question2.grid(row = 2, column = 1, sticky = "w")
        self.question3.grid(row = 3, column = 1, sticky = "w")

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
        return self.question1.slider.moved and self.question2.check() and self.question3.check()

    def back(self):
        self.warning.config(foreground = "red")

    def write(self):
        self.file.write(str(self.question1.slider.get()) + "\n")
        self.question2.write()
        self.question3.write()
        self.file.write(str(time()))

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

        self.num = 1

        q1 = ("Plánujeme další výzkum, ve kterém by nás zajímalo, jestli jsou preference "
              "u spotřebního zboží dlouhodobé. Výzkum by probíhal stejně jako ten, kterého  "
              "jste se právě účastnil(a) s jednou změnou. Program by během zdůvodňování Vaší "
              "volby zaměnil některé výrobky, které jste si vybral(a). Takže byste uváděl(a) důvody, "
              "proč jste si vybral(a) opačný výrobek z dvojice než ten, který jste si reálně zvolil(a). "
              "Myslíte si, že byste si takové záměny všiml(a)?")
        q2 = ("Kolik z 20 dvojic výrobků si myslíte, že by muselo být v takovém výzkumu zaměněno, "
              "abyste si takové záměny všiml(a)?")
        q3 = ("K takéto záměně došlo i při dnešním experimentu. Všiml(a) jste si jí v průběhu "
              "uvádění důvodů na počítači?")
        q4 = ('Označil(a) jste tyto zaměněné výrobky volbou možností '
              '"Vybral(a) bych si jinak / Spletl(a) jsem se"?')
        q4a = "Proč jste zaměněné výrobky takto neoznačil(a)?"
        self.question1 = Question(self, q1, label = False)
        self.question2 = Question(self, q2, width = 100, answer = (ttk.Entry, {"width": 5}))
        self.question3 = Question(self, q3, width = 90)
        self.question4 = Question(self, q4, (ttk.Entry, {"width": 100}), width = 90,
                                  condtype = "entry", condtext = q4a, condition = "no")

        self.question1.grid(row = 1, column = 1, sticky = "w")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.proceed)
        self.next.grid(row = 5, column = 1)

        self.warning = ttk.Label(self, text = "Odpovězte prosím na otázku.",
                                 background = "white", font = "helvetica 15", foreground = "white",
                                 width = 100, anchor = "center")
        self.warning.grid(row = 6, column = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 2)
        self.rowconfigure(4, weight = 2)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 2)
        self.rowconfigure(7, weight = 2)

        self.can1 = Canvas(self, background = "white", highlightbackground = "white", height = 130,
                           width = 1).grid(row = 1, column = 0, sticky = (N, S))
        self.can2 = Canvas(self,background = "white", highlightbackground = "white", height = 100,
                           width = 1).grid(row = 2, column = 0, sticky = (N, S))
        self.can3 = Canvas(self, background = "white", highlightbackground = "white", height = 100,
                           width = 1).grid(row = 3, column = 0, sticky = (N, S))
        self.can4 = Canvas(self, background = "white", highlightbackground = "white", height = 100,
                           width = 1).grid(row = 4, column = 0, sticky = (N, S))

        self.next.bind("<FocusIn>", lambda e: self.focus_set())

        
    def check(self):
        checks = sum((1 for i in range(4) if (self.question1.check(),
                                              self.question2.check(),
                                              self.question3.check(),
                                              self.question4.check())[i]))
        return checks == self.num

    def back(self):
        self.warning.config(foreground = "red")
       

    def proceed(self):
        if self.check():
            if self.num == 4:
                self.question4.write()
                self.file.write(str(time()))
                self.nextFun()
                return
            elif self.num == 3:
                self.question4.grid(row = 4, column = 1, sticky = "w")
                self.question3.disable()
                self.question3.write()
                self.file.write(str(time()) + "\n")
            elif self.num == 2:
                self.question3.grid(row = 3, column = 1, sticky = "w")
                self.question2.disable()
                self.question2.write()
                self.file.write(str(time()) + "\n")
            elif self.num == 1:
                self.question2.grid(row = 2, column = 1, sticky = "w")
                self.question1.disable()
                self.question1.write()
                self.file.write(str(time()) + "\n")
            self.num += 1
            self.warning.config(foreground = "white")
        else:
            self.back()                    








class Catches(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)

        self.file.write("\nCatches\t" + str(time()) + "\n")

        self.selected = []

        files = os.listdir(os.path.join(os.getcwd(), "Stuff"))
        files = [int(file.split("_")[0]) for file in files if file.endswith("_1.gif")]
        files = [file for file in files if file <= 12]

        random.shuffle(files)
                           
        self.pairs = {}
        for count, product in enumerate(files):
            c = random.randint(0, 1)
            self.pairs[product] = BorderCanvas(self)
            self.pairs[product].changeImages(product)
            self.pairs[product].grid(row = count % 5 + 1, column = (count // 5)*3 + c + 1,
                                     padx = 25, pady = 1)
            cplus = product + 12
            self.pairs[cplus] = BorderCanvas(self)
            self.pairs[cplus].changeImages(cplus)
            self.pairs[cplus].grid(row = count % 5 + 1, column = (count // 5)*3 + (1 - c) + 1,
                                   padx = 25, pady = 1)
            

        text = ("U kterých z dvojic výrobků podle Vás došlo k záměně?\n"
                "Označte všechny dvojice, u nichž si myslíte, že Vám byl k uvádění důvodů "
                "volby prezentován výrobek, jenž jste si nezvolil(a).")
        self.text = ttk.Label(self, font = "helvetica 16", justify = "center",
                              background = "white", text = text)
        self.text.grid(row = 0, column = 1, columnspan = 5, sticky = S, pady = 7)

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun)
        self.next.grid(row = 6, column = 2, columnspan = 3, pady = 2)

        self.columnconfigure(0, weight = 2)
        self.columnconfigure(3, weight = 3)
        self.columnconfigure(6, weight = 2)

    def proceed(self):
        pass

    def write(self):
        chosen = [k for k, v in self.pairs.items() if v.chosen]
        self.file.write("\t".join(map(str, chosen)))

    
             

class BorderCanvas(Canvas):
    def __init__(self, root):
        super().__init__(root, highlightbackground = "white")

        self.selected = []
        self.chosen = False

        self.bg = self.create_rectangle(0, 0, 380, 266, fill = "white", tag = "bg")

        self.products = TwoProducts(self, clickable = False, oneLabel = True, small = True)
        self.products.grid(padx = 3, pady = 3)

    def changeImages(self, product):
        self.products.changeImages(product)

    def clicked(self):
        if self.chosen:
            self.itemconfigure(self.bg, fill = "white")
        else:
            self.itemconfigure(self.bg, fill = "red")
        self.chosen = not self.chosen
            

             


        

class Demographics(ExperimentFrame):
    def __init__(self, root):
        super().__init__(root)
       
        self.sex = StringVar()
        self.student = StringVar()
        self.age = StringVar()
        self.file.write("Demographics\t{}\n".format(str(time())))

        self.lab1 = ttk.Label(self, text = "Jste:", background = "white",
                              font = "helvetica 15")
        self.lab1.grid(column = 1, row = 1, pady = 13, sticky = W, padx = 2)
        self.lab2 = ttk.Label(self, text = "Kolik je Vám let?", background = "white",
                              font = "helvetica 15")
        self.lab2.grid(column = 1, row = 2, pady = 13, sticky = W, padx = 2)        
        self.lab3 = ttk.Label(self, text = "Jste student(ka) VŠ?      ", background = "white",
                              font = "helvetica 15")
        self.lab3.grid(column = 1, row = 3, pady = 13, sticky = W, padx = 2)

        self.male = ttk.Radiobutton(self, text = "muž", variable = self.sex, value = "male",
                                    command = self.checkAllFilled)
        self.female = ttk.Radiobutton(self, text = "žena", variable = self.sex,
                                      value = "female", command = self.checkAllFilled)

        self.yes = ttk.Radiobutton(self, text = "Ano", variable = self.student,
                                   value = "student", command = self.checkAllFilled)
        self.no = ttk.Radiobutton(self, text = "Ne", variable = self.student,
                                  value = "nonstudent", command = self.checkAllFilled)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")
        ttk.Style().configure("TButton", font = "helvetica 15")

        self.ageCB = ttk.Combobox(self, textvariable = self.age, width = 6, font = "helvetica 14")
        self.ageCB["values"] = tuple([""] + [str(i) for i in range(18, 80)])
        self.ageCB.bind("<<ComboboxSelected>>", lambda e: self.checkAllFilled())

        self.male.grid(column = 2, row = 1, pady = 7, padx = 7, sticky = W)
        self.female.grid(column = 3, row = 1, pady = 7, padx = 7, sticky = W)
        self.yes.grid(column = 2, row = 3, pady = 7, padx = 7, sticky = W)
        self.no.grid(column = 3, row = 3, pady = 7, padx = 7, sticky = W)
        self.ageCB.grid(column = 2, row = 2, pady = 7, padx = 7, sticky = W)

        self.columnconfigure(5, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(5, weight = 1)

        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(row = 4, column = 0, pady = 20, columnspan = 6)


    def checkAllFilled(self, _ = None):
        if self.student.get() and self.age.get() and self.sex.get():
            self.next["state"] = "!disabled"

    def write(self):
        self.file.write(self.sex.get() + "\n")
        self.file.write(self.age.get() + "\n")
        self.file.write(self.student.get() + "\n")



def main():
    GUI()


if __name__ == "__main__":
    main()

