from music21 import *

k = key.Key("C")

print(k.mode)

k.tonic.octave = 4

csharp = note.Note("C#4")
print(csharp.name)
print(csharp.pitch.name)
print(csharp.octave)
print(csharp.pitch.octave)

c = chord.Chord("B4")

number = roman.romanNumeralFromChord(b, k).figure
r = roman.RomanNumeral(rn, k)

for p in r.pitches:
    name = p.name

