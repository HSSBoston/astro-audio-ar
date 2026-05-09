from music21 import *
import random, pprint
import numpy as np
from constants import *

def generateOneMeasureChordProgression(scorePart, numOfChords):
    
    if numOfChords == 1:
        chord1 = random.choice(CHORD_CHOICES)
        print(romanToChordTones[chord1])

        c1 = chord.Chord(romanToChordTones[chord1])
        c1.quarterLength = 4
        m1.append(oneChord)

    if numOfChords == 2:
        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c1.quarterLength = 2
        c2 = chord.Chord(romanToChordTones[chord2])
        c2.quarterLength = 2
        m1.append(c1)
        m1.append(c2)

    if numOfChords == 3:
        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])

        randomInt = random.randint(0,1)
        if randomInt <= 0.33:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarerLength = 1
        elif randomInt <= 0.66:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarerLength = 1
        else:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarerLength = 2

        m1.append(c1)
        m1.append(c2)
        m1.append(c3)

    if numOfChords == 4:

        chord1 = random.choice(CHORD_CHOICES)
        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])

        c1.quarterLength = 1
        c2.quarterLength = 1
        c3.quarterLength = 1
        c4.quarterLength = 1

        m1.append(c1)
        m1.append(c2)
        m1.append(c3)
        m1.append(c4)


    return scorePart


def generateTwoMeasureChordProgression(scorePart, numOfChords):
    #minimum 2 chords
    if numOfChords == 2:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])

        c1 = chord.Chord(romanToChordTones[chord1])
        c1.quarterLength = 4
        c2 = chord.Chord(romanToChordTones[chord2])
        c2.quarterLength = 4
        m1.append(c1)
        m2.append(c2)

    if numOfChords == 3:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])

        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        while not (chord3 in ["I", "V", "VI"]):
            chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])

        randomInt = random.randint(0,1)
        if randomInt <= 0.5:
            c1.quarterLength = 2
            c2.quarterLength = 2
            c3.quarerLength = 4
            m1.append([c1,c2])
            m2.append(c3)
        else:
            c1.quarterLength = 4
            c2.quarterLength = 2
            c3.quarerLength = 2
            m1.append(c1)
            m2.append([c2,c3])


    if numOfChords == 4:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])
        while not (chord4 in ["I", "V", "VI"]):
            chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])

        randomInt = random.randint(0,1)
        if randomInt <= 0.5:
            c1.quarterLength = 2
            c2.quarterLength = 2
            c3.quarterLength = 2
            c4.quarterLength = 2
        else:
            randomInt = random.randint(0,1)
            if randomInt <= 0.2:
                c1.quarterLength = 1
                c2.quarterLength = 1
                c3.quarterLength = 2
                c4.quarterLength = 4
                m1.append([c1,c2,c3])
                m2.append(c4)
            elif randomInt <= 0.4:
                c1.quarterLength = 2
                c2.quarterLength = 1
                c3.quarterLength = 1
                c4.quarterLength = 4
                m1.append([c1,c2,c3])
                m2.append(c4)
            elif randomInt <= 0.6:
                c1.quarterLength = 1
                c2.quarterLength = 2
                c3.quarterLength = 1
                c4.quarterLength = 4
                m1.append([c1,c2,c3])
                m2.append(c4)
            elif randomInt <= 0.75:
                c1.quarterLength = 4
                c2.quarterLength = 1
                c3.quarterLength = 1
                c4.quarterLength = 2
                m1.append(c1)
                m2.append([c2,c3,c4])
            elif randomInt <= 0.9:
                c1.quarterLength = 4
                c2.quarterLength = 1
                c3.quarterLength = 2
                c4.quarterLength = 1
                m1.append(c1)
                m2.append([c2,c3,c4])
            else:
                c1.quarterLength = 4
                c2.quarterLength = 2
                c3.quarterLength = 1
                c4.quarterLength = 1
                m1.append(c1)
                m2.append([c2,c3,c4])


    if numOfChords == 5:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])
        chord5 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord4]])
        while not (chord5 in ["I", "V", "VI"]):
            chord5 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord4]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])
        c5 = chord.Chord(romanToChordTones[chord5])

        randomInt = random.randint(0,1)
        if randomInt <= 0.17:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 2
            c4.quarterLength = 2
            c5.quarterLength = 2
            m1.append([c1,c2,c3])
            m2.append([c4,c5])
        elif randomInt <= 0.34:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 2
            c5.quarterLength = 2
            m1.append([c1,c2,c3])
            m2.append([c4,c5])
        elif randomInt <= 0.51:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 2
            c5.quarterLength = 2
            m1.append([c1,c2,c3])
            m2.append([c4,c5])
        elif randomInt <= 0.68:
            c1.quarterLength = 2
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 2
            m1.append([c1,c2])
            m2.append([c3,c4,c5])
        elif randomInt <= 0.85:
            c1.quarterLength = 2
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 2
            c5.quarterLength = 1
            m1.append([c1,c2])
            m2.append([c3,c4,c5])
        else:
            c1.quarterLength = 2
            c2.quarterLength = 2
            c3.quarterLength = 2
            c4.quarterLength = 1
            c5.quarterLength = 1
            m1.append([c1,c2])
            m2.append([c3,c4,c5])

    if numOfChords == 6:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])
        chord5 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord4]])
        chord6 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord5]])
        while not (chord6 in ["I", "V", "VI"]):
            chord6 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord5]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])
        c5 = chord.Chord(romanToChordTones[chord5])
        c6 = chord.Chord(romanToChordTones[chord6])

        randomInt = random.randint(0,1)

        #ending 1 1 2
        if randomInt <= 0.11:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 2
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 2
        elif randomInt <= 0.22:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 2
        elif randomInt <= 0.33:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 2

        #ending in 1 2 1
        elif randomInt <= 0.44:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 2
            c4.quarterLength = 1
            c5.quarterLength = 2
            c6.quarterLength = 1
        elif randomInt <= 0.55:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 2
            c6.quarterLength = 1
        elif randomInt <= 0.66:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 2
            c6.quarterLength = 1

        #ending in 2 1 1
        elif randomInt <= 0.77:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 2
            c4.quarterLength = 2
            c5.quarterLength = 1
            c6.quarterLength = 1
        elif randomInt <= 0.88:
            c1.quarterLength = 1
            c2.quarterLength = 2
            c3.quarterLength = 1
            c4.quarterLength = 2
            c5.quarterLength = 1
            c6.quarterLength = 1
        else:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 2
            c5.quarterLength = 1
            c6.quarterLength = 1

        m1.append([c1,c2,c3])
        m2.append([c4,c5,c6])

    if numOfChords == 7:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])
        chord5 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord4]])
        chord6 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord5]])
        chord7 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord6]])
        while not (chord7 in ["I", "V", "VI"]):
            chord7 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord6]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])
        c5 = chord.Chord(romanToChordTones[chord5])
        c6 = chord.Chord(romanToChordTones[chord6])
        c7 = chord.Chord(romanToChordTones[chord7])

        randomInt = random.randint(0,1)

        if randomInt <= 0.25:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 1
            c7.quarterLength = 2
            m1.append([c1,c2,c3,c4])
            m2.append([c5,c6,c7])
        elif randomInt <= 0.5:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 2
            c6.quarterLength = 1
            c7.quarterLength = 1
            m1.append([c1,c2,c3,c4])
            m2.append([c5,c6,c7])
        elif randomInt <= 0.75:
            c1.quarterLength = 1
            c2.quarterLength = 1
            c3.quarterLength = 2
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 1
            c7.quarterLength = 1
            m1.append([c1,c2,c3])
            m2.append([c4,c5,c6,c7])
        else:
            c1.quarterLength = 2
            c2.quarterLength = 1
            c3.quarterLength = 1
            c4.quarterLength = 1
            c5.quarterLength = 1
            c6.quarterLength = 1
            c7.quarterLength = 1
            m1.append([c1,c2,c3])
            m2.append([c4,c5,c6,c7])

    if numOfChords == 8:

        chord1 = random.choice(CHORD_CHOICES)
        while chord1 == "VII":
            chord1 = random.choice(CHORD_CHOICES)

        chord2 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord1]])
        chord3 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord2]])
        chord4 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord3]])
        chord5 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord4]])
        chord6 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord5]])
        chord7 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord6]])
        chord8 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord7]])
        while not (chord8 in ["I", "V", "VI"]):
            chord8 = rng.choice(["I", "II", "IV", "V", "VI", "VII"], p=P[romanToIndex[chord7]])


        c1 = chord.Chord(romanToChordTones[chord1])
        c2 = chord.Chord(romanToChordTones[chord2])
        c3 = chord.Chord(romanToChordTones[chord3])
        c4 = chord.Chord(romanToChordTones[chord4])
        c5 = chord.Chord(romanToChordTones[chord5])
        c6 = chord.Chord(romanToChordTones[chord6])
        c7 = chord.Chord(romanToChordTones[chord7])
        c8 = chord.Chord(romanToChordTones[chord8])

        c1.quarterLength = 1
        c2.quarterLength = 1
        c3.quarterLength = 1
        c4.quarterLength = 1
        c5.quarterLength = 1
        c6.quarterLength = 1
        c7.quarterLength = 1

        m1.append([c1,c2,c3,c4])
        m2.append([c5,c6,c7,c8])

    return scorePart


