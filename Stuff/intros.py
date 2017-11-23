from common import InstructionsFrame
from math import ceil
import random


intro = """
Dobrý den,

děkujeme, že se účastníte našeho výzkumu. Studie sestává z několika samostatných částí, v jejichž průběhu budete na počítači řešit různé úlohy a odpovídat na otázky. Celá studie trvá asi 50 minut.

Vaše účast na výzkumu je zcela dobrovolná a můžete ji kdykoliv ukončit. Pokud se budete chtít na něco zeptat, přivolejte prosím experimentátora zvednutím ruky.

Kliknutím na tlačítko Pokračovat vyjadřujete svůj souhlas s účastí a anonymním využitím Vašich dat.

Pro začátek klikněte na tlačítko Pokračovat.
"""



endingtext = """
Děkujeme za Vaši účast!

Dnešní výzkum sestával z několika samostatných studií:
Dva experimenty se zabývaly morálním usuzováním. Vaším úkolem bylo odpovídat, do jaké míry považujete popsaná chování za špatná. Nás zajímal vliv časového tlaku a nutnosti obhajovat svoje rozhodnutí na Vaše morální úsudky. 
V dalším experimentu jste měli vybírat, která kostka byla blíže dříve zobrazenému křížku. V tomto experimentu sledujeme, jestli volbu nějak ovlivní odměna, která je s ní spjatá.
V jiném experimentu bylo Vaším úkolem porovnávat čas zobrazení dvou čtverců. Nás zajímalo, jestli vnímání času ovlivňuje barva a pozice čtverce.
V experimentu, kde jste porovnávali, nakolik se Vám líbí dva rytmy, jsme testovali, zda lidé mají stejné preference u nižších frekvencí, jako byly dříve nalezeny u frekvencí vyšších.

Podrobnější popis jednotlivých studií a jejich hypotéz Vám bude zaslán v průběhu nejbližších dní e-mailem. Prosíme, abyste tyto informace během sběru dat nešířili, zejména ne mezi potenciální účastníky. O ukončení sběru dat budete informováni rovněž e-mailem.

{}

Nyní si můžete vzít své věci, papírek s číslem pracovního místa a výší odměny a přejít do vedlejší místnosti, kde Vám bude odměna vyplacena. 
Tím Vaše účast na dnešní studii končí. Ještě jednou děkujeme!
"""

winending = "V loterii jste byl/a vylosován/a a z vybraných produktů si tedy jako výhru tři odnesete. Na papírek ležící na stole napište číslo Vašeho pracovního místa a níže uvedené kódy vyhraných produktů:\n{}\n{}\n{}"
lostending = "V loterii jste nebyl/a vylosován/a a bohužel si tedy domů vybrané produkty neodnesete."

Intro =(InstructionsFrame, {"text": intro})



class Ending(InstructionsFrame):
    def __init__(self):
        pass
    
    def __call__(self, root):
        win = random.random() < 1/5
        if win:
            keys = [key for key in root.selected.keys()]
            keys = random.sample(keys, 3)
            prize = []
            for key in keys:
                prize.append(key + "-" + random.choice(root.selected[key]))
            root.file.write("Won products\n" + "\n".join(prize))
            text = endingtext.format(winending.format(*prize))
        else:
            text = endingtext.format(lostending)
        super().__init__(root, text, height = 30, font = 15, proceed = False)
        return self

ending = Ending()
