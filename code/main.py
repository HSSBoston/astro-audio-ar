from music21 import *
import random, pprint
import numpy as np
from constants import *
from chord_progression import *

# melody = stream.Part()
# m1Chord = stream.Measure()
#
# m1Melody = stream.Measure()
# m1Chord.timeSignature = meter.TimeSignature()
# m1Melody.timeSignature = meter.TimeSignature()
# m1Chord.keySignature = key.Key(KEY_CHOICE)
# m1Melody.keySignature = key.Key(KEY_CHOICE)
# m2Chord = stream.Measure()
# m2Melody = stream.Measure()
# m2Chord.rightBarLine = bar.Barline("final")
# m2Melody.rightBarLine = bar.Barline("final")
#
# chords = stream.Part()

randomInt = random.randint(0,1)

# if randomInt <= 0.25:
numOfChords = 4
numOfMeasures = 1
# elif randomInt <= 0.5:
#     numOfChords = 2
# elif randomInt <= 0.75:
#     numOfChords = 3
# else:
#     numOfChords = 4

scorePart = stream.Part()
m1 = stream.Measure()
m1.TimeSignature = meter.TimeSignature("4/4")
m1.keySignature = key.Key(KEY_CHOICE)
scorePart.append(m1)

if numOfMeasures == 1:
    temp = tempo.MetronomeMark("adagio")
    m1.append(temp)
    m1.rightBarLine = bar.Barline("final")
    print( len(scorePart) )
#     scorePart = generateOneMeasureChordProgression(scorePart, numOfChords)
if numOfMeasures == 2:
    m2 = stream.Measure()
    scorePart.append(m2)    
    scorePart = generateTwoMeasureChordProgression(scorePart, numOfChords)

scorePart.show()









# count = 0
# for num in PROGRESSION:
#   count += 1
#   print(romanToChordTones[num])
#   print(romanToChordTonesMidi[num])
#   c = chord.Chord(romanToChordTones[num])
#   c.quarterLength = 2
#   if count <= 2:
#     m1Chord.append(c)
#   else:
#     m2Chord.append(c)
#
# chords.append([m1Chord,m2Chord])
# melody.append(note.Note("G"))
# s = stream.Score([melody,chords])
# s.show()

