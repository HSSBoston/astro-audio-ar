from music21 import *

p1 = pitch.Pitch('b-4')
print(p1.octave)
print(p1.pitchClass)
print(p1.name)
print(p1.accidental.alter)
print(p1.nameWithOctave)
print(p1.midi) #print the midi number/index

p1.name = "d#" #change the pitch of p1
p1.octave = 3
print(p1.nameWithOctave)

p2 = p1.transpose("M7")
print(p2)

#pitch is essetially same attributes and methods as note
csharp = note.Note("C#4")
print(csharp.name)
print(csharp.pitch.name)
print(csharp.octave)
print(csharp.pitch.octave)

#things pitch can do that notes can't
print(csharp.pitch.unicodeName)
print(csharp.pitch.getEnharmonic()) #method to get enharmonic
print(csharp.pitch.getLowerEnharmonic())

halfDuration = duration.Duration("half") # "Half" is the type of the Duration
#Duration types: "whole", "half", "quarter", "eighth", "16th", "32nd", "64th"
dottedQuarter = duration.Duration(1.5)
#padd in a number to represent how many quarter notes long it is
print(dottedQuarter.quarterLength)#print how many quarter notes
print(halfDuration.quarterLength)
print(dottedQuarter.dots)#print how many dots in duration

otherNote = note.Note("F6")
otherNote.lyric = "I'm the Queen of the Night!" #can assign lyrics to notes

n1 = note.Note("E5")
n1.addLyric(n1.nameWithOctave)
n1.addLyric(n1.pitch.pitchClassString)
n1.addLyric(f"QL: {n1.quarterLength}")
n1.show()