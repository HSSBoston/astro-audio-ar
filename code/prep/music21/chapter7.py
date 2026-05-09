from music21 import *

cMajor = chord.Chord(["C4","E4","G4"])
#chords have pitches
print(cMajor.pitches)

print(cMajor.isMinorTriad())
print(cMajor.isMajorTriad())

cMajor6 = chord.Chord(["E4","G4","C5"])
print(cMajor6.inversion())

print(cMajor.root()) #method
print(cMajor.third) #not method
print(cMajor.fifth)

cMajor.add("C5")
print(cMajor.pitches)
#cMajor.show()

#there is a closedPosition() method to get rid of unecessary "space"/octaves between notes

gMajor= chord.Chord([note.Note("G4"), note.Note("B4"), note.Note("D5")]) #create chord with list
fMajor = chord.Chord("F4 A4 C4") #or with string with space

rest1 = note.Rest()
rest1.quarterLength = 0.5
noteASharp = note.Note('G5')
noteASharp.quarterLength = 1.5

stream2 = stream.Stream()
stream2.append(gMajor)
stream2.append(rest1)
stream2.append(noteASharp)
stream2.show()