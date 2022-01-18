def FindLetter1(aWords, aFind):
    i = 0
    counter1 = 0
    while(i<len(aWords)):
        Leter = aWords[i]
        if(Leter == aFind):    
            #print (Leter)
            counter1 += 1
        i += 1
    print (aFind, counter1)


Words = 'Hello world. Ok!'
#FindLetter1(Words, 'o')
#FindLetter1(Words, 'l')
#FindLetter1(Words, 'r')
#FindLetter1(Words, 'e')

#for Letter in ['o', 'l', 'r', 'e']:
#    FindLetter1(Words, Letter)

for Letter in Words:
    FindLetter1(Words, Letter)
