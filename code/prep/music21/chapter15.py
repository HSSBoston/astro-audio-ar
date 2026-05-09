from music21 import *

ks1 = key.KeySignature(2) #argument is number of sharps
print(ks1.sharps)
print(ks1.alteredPitches) #in circle of fifth order
print(ks1.accidentalByStep("C")) #print accdiental for given step
print(ks1.accidentalByStep("E"))

ks2 = ks1.transpose("M2") #moves ks1 (all pitches and notes) up a M2
print(ks2)

print(ks1.getScale("major")) #find corresponding major or minor scale
print(ks1.getScale("minor"))

m = stream.Measure()
m.insert(0, meter.TimeSignature('3/4'))
m.insert(0, ks1) #use .insert() method to set keysignature
d = note.Note('D')
c = note.Note('C')
fis = note.Note('F#') # German name
m.append([d, c, fis])
#m.show()

ks3 = key.KeySignature (-3) # use negative numbers to indicate flats
print(ks3)

#these 2 measures have lots of accidentals that make it hard to play
#so we can "fix" it by making all the notes to fit the key sig.
m1 = stream.Measure() 
m1.timeSignature = meter.TimeSignature('2/4')
m1.keySignature = key.KeySignature(-5) #Gb major
m1.append([note.Note('D'), note.Note('A')]) #D and A natural in Gb major
m2 = stream.Measure()
m2.append([note.Note('B-'), note.Note('G#')]) #G sharp in Gb major
p = stream.Part()
p.append([m1, m2])

ks = m1.keySignature
for n in p.recurse().notes:  #we need to recurse because the notes are in measures
    nStep = n.pitch.step #each notes
    rightAccidental = ks.accidentalByStep(nStep) #get the intended accidental from the key
    n.pitch.accidental = rightAccidental #make the accidental of n (an attribute of n) into the right one
# p.show()


kD = key.Key("D") #don't have to make key with number of sharps/flats
print(kD) #use upper case for major

bFlat = pitch.Pitch("B-") 
kBflat = key.Key(bFlat)
print(kBflat)

kg = key.Key("g") #use lower for minor
print(kg)
kd = key.Key('D', 'minor') #or add argument
print(kd)

print(ks1.asKey("major"), ks1.asKey("minor")) #make KeySignature objects into Key objects
print(kg.mode)
print(kg.relative)
print(kg.parallel)

bach = corpus.parse('bwv66.6')
bach.id = 'bach66'
fis = bach.analyze('key') # can analyze excerpts to find key
print(fis.correlationCoefficient) # find the certainty measure
print(fis.alternateInterpretations[0:4] )# the alternative/the keys the piece coudl have been in

