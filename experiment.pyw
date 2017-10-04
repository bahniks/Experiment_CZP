#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))

from gui import GUI

from intros import Intro, ending
from dicehonesty import DiceTrialOne, DiceExperiment, DiceTrialTwo
from dicehonesty import DiceInstructions1, DiceInstructions2, DiceInstructions3
from music import Music, MusicIntro, MusicOutro
from moraltime import MoralTime, MoralTimeInstructions
from timing import TimeOne, TimeTwo, TimingPause, TimingInstructions, TimingOutro
from account import Account, AccountInstructions
from quest import Hexaco, Prosociality, QuestInstructions
from politics import Politics
from debrief import Debriefing
from demo import Demographics
from comments import Comments


frames = [Intro,
          DiceInstructions1,
          DiceTrialOne,
          DiceInstructions2,
          DiceExperiment,
          DiceInstructions3,
          DiceTrialTwo,
          MusicIntro,
          Music,
          MusicOutro,
          MoralTimeInstructions,
          MoralTime,
          TimingInstructions,
          TimeOne,
          TimingPause,
          TimeTwo,
          TimingOutro,
          AccountInstructions,
          Account,
          QuestInstructions,
          Hexaco,
          Prosociality,
          Politics,
          Debriefing,
          Demographics,
          Comments,
          ending
          ]



GUI(frames)
