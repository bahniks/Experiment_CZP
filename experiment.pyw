#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from blindness import ChoiceBlindnessInstructions1, ChoiceBlindness1, ChoiceBlindnessInstructions2
from blindness import ChoiceBlindness2, ChoiceBlindnessInstructions3, DebriefingOne, DebriefingTwo
from products import Choices, ProductsIntro
from mfq import MFQ1, MFQ2
from intros import ending, Intro, Debriefing
from comments import Comments
from demo import Demographics
from validation import Validation
from iat import Instructions, IAT, Introduction
from character import CharacterIntro, Character


frames = [Intro,
          Validation,
          ChoiceBlindnessInstructions1, # choice blindness
          ChoiceBlindness1,
          ChoiceBlindnessInstructions2,
          ChoiceBlindness2,
          ChoiceBlindnessInstructions3,
          Introduction, # IAT
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
          IAT,
          CharacterIntro, # credentials/credits
          Character,
          MFQ1, # moral foundations questionnaire
          MFQ2,
          ProductsIntro, # choice of products
          Choices, 
          DebriefingOne, # debriefing for choice blindness
          DebriefingTwo,
          Demographics,
          Comments,
          Debriefing,
          ending
         ]


with open("start.txt") as f:
    startingFrame = f.readline().strip()
    frames = frames[int(startingFrame):]
    
GUI(frames)

text = ""
with open("start.txt") as f:
    for num, line in enumerate(f):
        if num == 0:
            text += "0\n"
        else:
            text += line

with open("start.txt", mode = "w") as f:
    f.write(text)
