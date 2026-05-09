from music21 import *

stream1 = stream.Stream() #use to store notes by appending
note1 = note.Note("C4")
stream1.append(note1)
n2 = note.Note("E4")
stream1.append(n2)
n3 = note.Note("G4")
stream1.append(n3)
n4 = note.Note("C5")
stream1.append(n4)
#stream1.repeatAppend(n2, 3) #to store multiple copies of same note
stream1.show()

print(len(stream1)) #number of notes
print(stream1.show("text"))

for thisNote in stream1:
    print(thisNote.step)
    
print(stream1[0]) #like a list
n2Index = stream1.index(note1)
#stream1.pop(n2Index) #remove an element from stream
#stream1.show()

for thisNote in stream1.getElementsByClass(note.Note): #iterates through every note object
    print(thisNote, thisNote.offset)
    
for thisNote in stream1.notes: # same thing
    print(thisNote)
    
print(stream1.pitches) #prints out a list of notes

print(stream1.analyze("ambitus")) # finds the range from the lowest to highest note

print(n2.offset)

biggerStream = stream.Stream() # can put streams into streams

cNote = note.Note("C3")
biggerStream.insert(cNote)
biggerStream.append(stream1)
#biggerStream.show()