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

dilemmasintro = """
Nyní budete číst krátké popisy několika situací a činů, jež různé osoby v těchto situacích vykonají nebo mohou vykonat.

Při čtení můžete mít někdy pocit, že situace, tak jak jsou popsané, nejsou realistické. Například můžete číst, že když osoba udělá X, stane se Y, a můžete si myslet, že to není realistické – tedy že nemusí nutně dojít k Y, pokud osoba udělá X. V případě, že budete mít takovéto pochybnosti, prosíme potlačte je, jako byste to udělal(a) například u ne zcela realistického filmu a předpokládejte, že situace se odehrají tak, jak jsou popsány.

Čtěte prosím pozorně popisy všech situací a odpovězte na otázky, jež budou po každé situaci následovat.
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

V experimentu s porovnáváním času zobrazení čtverců jste ze 100 párů čtverců správně rozpoznal/a déle zobrazený čtverec v {} případech. Pokud jste tak již neučinil/a, zapište si prosím toto číslo na papír k číslu Vašeho místa a výši odměny. 

Nyní si můžete vzít své věci, papírek s číslem pracovního místa a výší odměny a přejít do vedlejší místnosti, kde Vám bude odměna vyplacena. 
Tím Vaše účast na dnešní studii končí. Ještě jednou děkujeme!
"""

winending = "V loterii jste byl/a vylosován/a a za první úkol tak získáváte pro sebe navíc {} Kč a pro charitu {} Kč. Vaše celková odměna je tedy {} Kč. Na papírek ležící na stole napište číslo Vašeho pracovního místa a celkovou výši odměny pro sebe a pro charitu."
lostending = "V loterii jste nebyl/a vylosován/a a Vaše celková odměna je tedy 100 Kč. Na papírek ležící na stole napište číslo Vašeho pracovního místa a výši odměny."

Intro =(InstructionsFrame, {"text": intro})
DilemmasIntro = (InstructionsFrame, {"text": dilemmasintro})


class Ending(InstructionsFrame):
    def __init__(self):
        pass
    
    def __call__(self, root):
        win = random.random() < 1/5
        if win:
            reward = ceil(int(root.reward)/10)*10
            charity = ceil(int(root.charity)/10)*10
            text = endingtext.format(winending.format(reward, charity, reward + 100), root.timingCorrect)
        else:
            text = endingtext.format(lostending, root.timingCorrect)
        super().__init__(root, text, height = 30, font = 15, proceed = False)
        return self

ending = Ending()
