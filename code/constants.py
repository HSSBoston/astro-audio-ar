from music21 import *
import random, pprint
import numpy as np

KEY_CHOICE = "C"
#PROGRESSION = ["I", "IV", "V", "I"]
CHORD_CHOICES = ["I","II","IV","V","VI","VII",]
RANDOM_SEED = None #None or int
rng = np.random.default_rng(seed=RANDOM_SEED)

P = np.array(
    [[0.16, 0.16, 0.16, 0.2, 0.16, 0.16],
     [0.1, 0.1, 0, 0.35, 0.1, 0.35],
     [0.2, 0.2, 0.2, 0.2, 0.05, 0.15],
     [0.4, 0, 0, 0.1, 0.4, 0.1],
     [0, 0.3, 0.3, 0.3, 0.05, 0.05],
     [1, 0, 0, 0, 0, 0]
    ])

k = key.Key(KEY_CHOICE)
#print(k)

if k.mode == "major":
  sc = scale.MajorScale(KEY_CHOICE)
else:
  sc = scale.MinorScale(KEY_CHOICE)

scalePitchNames = [p.nameWithOctave for p in sc.getPitches()]
scaleMidi       = [p.midi           for p in sc.getPitches()]
scalePitchNames = scalePitchNames[0:-1]
scaleMidi       = scaleMidi[0:-1]
#print(scalePitchNames)
#print(scaleMidi)

if k.mode == "major":
    rn1 = roman.RomanNumeral("I", sc)
    rn2 = roman.RomanNumeral("ii", sc)
    rn4 = roman.RomanNumeral("IV", sc)
    rn5 = roman.RomanNumeral("V", sc)
    rn6 = roman.RomanNumeral("vi", sc)
    rn7 = roman.RomanNumeral("viio", sc)
else:
    rn1 = roman.RomanNumeral("i", sc)
    rn2 = roman.RomanNumeral("iio", sc)
    rn4 = roman.RomanNumeral("iv", sc)
    rn5 = roman.RomanNumeral("v", sc)
    rn6 = roman.RomanNumeral("VI", sc)
    rn7 = roman.RomanNumeral("VII", sc)

romanToChordTones = {
    "I":  [p.nameWithOctave for p in rn1.pitches],
    "II": [p.nameWithOctave for p in rn2.pitches],
    "IV": [p.nameWithOctave for p in rn4.pitches],
    "V":  [p.nameWithOctave for p in rn5.pitches],
    "VI": [p.nameWithOctave for p in rn6.pitches],
    "VII":[p.nameWithOctave for p in rn7.pitches],
    }
romanToChordTonesMidi = {
    "I":  [p.midi for p in rn1.pitches],
    "II": [p.midi for p in rn2.pitches],
    "IV": [p.midi for p in rn4.pitches],
    "V":  [p.midi for p in rn5.pitches],
    "VI": [p.midi for p in rn6.pitches],
    "VII":[p.midi for p in rn7.pitches],
    }
romanToIndex = {
    "I":   0,
    "II":  1,
    "IV":  2,
    "V":   3,
    "VI":  4,
    "VII": 5,
}
