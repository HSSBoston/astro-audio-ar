from music21 import *
f = chord.Chord('F4 C5 A5')
kf = key.Key('F')
sf = stream.Measure([kf, f])
#sf.show()

kc = key.Key('C')
sc = stream.Part([kc, f])

kb = key.Key('B')
sb = stream.Part([kb, f])

#three different keys
rf = roman.romanNumeralFromChord(f,kf) #roman numeral of chord f in key of kf
rc = roman.romanNumeralFromChord(f,kc) #from key of kc
rb = roman.romanNumeralFromChord(f, kb) #from key of kb
print(rf) 
print(rc) 
print(rb) 

print(rf.figure, rc.figure, rb.figure) # numbers
print(rf.figureAndKey)
print(rf.scaleDegree, rc.scaleDegree, rb.scaleDegree) #doesn't print out the flat for rb so use the following
print(rb.scaleDegreeWithAlteration)
print(rf.functionalityScore, rc.functionalityScore, rb.functionalityScore) #prints out how "function" the chord is

rf2 = roman.RomanNumeral('I', kf)
print(rf2)
print(rf2.pitches)
#rf2.show()

subDom7 = roman.RomanNumeral("IV7", "B-")
#subDom7.show()

print(subDom7.figuresWritten) #prints out just the figures like the 7ths or inversions


rb.lyric = rb.figure #add lyric to write figure beneath chord
#rb.show() 