#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from blindness import ChoiceBlindnessInstructions1, ChoiceBlindness1, ChoiceBlindnessInstructions2
from blindness import ChoiceBlindness2, ChoiceBlindnessInstructions3, DebriefingOne, DebriefingTwo


frames = [ChoiceBlindnessInstructions1,
         ChoiceBlindness1,
         ChoiceBlindnessInstructions2,
         ChoiceBlindness2,
         ChoiceBlindnessInstructions3,
         DebriefingOne,
         DebriefingTwo
         ]



GUI(frames)
