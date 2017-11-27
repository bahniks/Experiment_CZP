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

debriefingtext = """
Dnešní výzkum sestával z několika samostatných studií:

Elektronický dotazník, který jste vyplňoval(a) před několika dny sloužil k měření postojů k životnímu prostředí.

První dva úkoly v experimentu se týkaly tzv. slepoty k volbě. Je to známý a dnes už relativně dobře popsaný jev, který spočívá v tom, že lidé dělají určité volby, aniž by měli jednoznačně vyhraněné preference a následně dokáží jen obtížně odhalit, když se jejich původní volba změní. Nás zajímalo, jestli tento proces probíhá odlišně u popisu vlastního chování a u hodnocení chování. 

Následující experiment se týkal toho, jestli mají lidé tendenci hodnotit nemorální chování druhých pozitivněji, pokud takoví lidé současně chrání životní prostředí. Tento experiment testuje hypotézy odvozené z teorie morální licence.

Poslední úkol, při němž jste si vybíral(a) výrobky sloužil ke zkoumání vašich preferencí s ohledem na cenu, množství a další charakteristiky výrobků (např. jejich zelený profil). 

Pro pokračování klikněte na tlačítko Pokračovat.
"""


endingtext = """
Děkujeme za Vaši účast!

Prosíme, abyste informace o těchto experimentech nešířil(a) během následujících 3 měsíců. Zejména Vás žádáme, abyste tyto informace nešířil(a) mezi potenciální účastníky a účastnice těchto experimentů. 

{}

Nyní si můžete vzít své věci a přejít do vedlejší místnosti, kde Vám bude vyplacena odměna. 
Tím Vaše účast na dnešní studii končí. Ještě jednou děkujeme!
"""

winending = "V loterii jste byl(a) vylosován(a) a z vybraných produktů si tedy jako výhru tři odnesete. Z výrobků, které jste si vybral(a), byly tři náhodně vylosovány. Na papírek ležící na stole napište číslo Vašeho pracovního místa a níže uvedené kódy vyhraných produktů:\n{}\n{}\n{}\n\nPapírek si s sebou vezměte a předejte ho experimentátorovi."
lostending = "V loterii jste nebyl(a) vylosován/a a bohužel si tedy domů vybrané produkty neodnesete. Dostanete však samozřejmě svou řádnou odměnu za účast v experimentu."


Intro =(InstructionsFrame, {"text": intro})
Debriefing =(InstructionsFrame, {"text": debriefingtext, "height": 22})


class Ending(InstructionsFrame):
    def __init__(self):
        pass
    
    def __call__(self, root):
        win = random.random() < 1/8
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
