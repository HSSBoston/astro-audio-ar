listA = [10, 20, 30]
listB = [1, 2, 3, listA]

#print(listB[3][2])# get third element of fourth element of listB

#to print all elements of listB
for thing in listB:
    if isinstance(thing, list): #the isinstance method takes looks at thing and if in list then do actions
        for number in thing:
            print(number)
    else:
        print(thing)
        
