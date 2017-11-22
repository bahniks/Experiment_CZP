#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from blindness import ChoiceBlindnessInstructions1, ChoiceBlindness1, ChoiceBlindnessInstructions2
from blindness import ChoiceBlindness2, ChoiceBlindnessInstructions3, DebriefingOne, DebriefingTwo
from products import Choices
from mfq import MFQ1, MFQ2
from IAT import Introduction, Instructions, IAT
from intros import ending, Intro
from comments import Comments
from demo import Demographics


frames = [Intro,
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
          Choices, # choice of products
          MFQ1, # moral foundations questionnaire
          MFQ2,
          DebriefingOne, # debriefing for choice blindness
          DebriefingTwo,
          Demographics,
          Comments,
          ending
         ]



GUI(frames)
