from music21 import *

#print(type(note))

f = note.Note("F5")
print(f.name)
print(f.octave)
print(f.pitch)
print(f.pitch.frequency)
print(f.pitch.pitchClass) #pitch class - C=0, C# and Db = 1, etc.
print(f.pitch.pitchClassString) #print as a string

bflat = note.Note("B-2") #flats are dashes(-)

acc = bflat.pitch.accidental #acc is of Accidental class
#Accidentals are negative if flat, plus if sharp, and None if no accidental
print(acc.alter) #print how many semitones acc has

f.show()

d = bflat.transpose("M3") #creates a new note.Note object that is M3 above bflat
bflat.transpose("P4", inPlace=True) #changes bflat itself

r = note.Rest()
