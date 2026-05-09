from music21 import *

sBach = corpus.parse('bach/bwv57.8') #get the chorale score
print(len(sBach.getElementsByClass(stream.Part))) # find how many parts (voices)
#how many measure in first part (soprano)
print(len(sBach.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure)))
#how many notes in the second measure in the soprano part
print(len(sBach.getElementsByClass(stream.Part)[0].getElementsByClass(
        stream.Measure)[1].getElementsByClass(note.Note)))

alto = sBach.parts[1]  # parts count from zero, so soprano is 0 and alto is 1
excerpt = alto.measures(1, 4)
#excerpt.show()
measure2 = alto.measure(2)  # measure not measure_s_
#measure2.show()
measureStack = sBach.measures(2, 3)
measureStack.show()

#.recurse() method to get to visit every element of a stream (use for loops)

