Numbers = ['Null', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine' ]
#print('Array length', len(Numbers))

#print(Numbers[0])
#print(Numbers[1])
#print(Numbers[2])
#print(Numbers[3])
#print(Numbers[4])
#print(Numbers[5])
#print(Numbers[6])
#print(Numbers[7])
#print(Numbers[8])
#print(Numbers[9])

a = False
i = 0
while (i < 10):
    print(i, a)
    i += 1
    a = not a

Digits = [0, 1, 2, 3, 4, 5]
#Digits = list(range(50))
#print(Digits)

#for D in Digits:
#     print(D)
#print('the end')

#for D in range(5):
#     print(D)

#a1 = 0
#for Number in Numbers:
#     print(Numbers[a1])
#     a1 += 1

#D = 0
#while (D < 20):
#     print(D)
#     #D = D + 1
#     #D += 1
#
#     D = D + 2

#D = 5
#while (D < 20):
#     print(D)
#     D = D + 5

#D = 20 
#while (D >= -1):
#while (D >= 0):
#     print(D*2)
#     if (D == 15) or (D == 5):
#          print('hello', D)
#     D = D - 5

#D = 20 
#while (D >= 0):
#     print(D * 2)
#     D = D - 5


Numbers = ['Null', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine' ]
#print(len(Numbers), Numbers[1])

#D = 0
#while (D < len(Numbers)):
#     print(D, Numbers[D])
#     D += 2

#D = len(Numbers) - 1
#while (D >= 0):
#     print(D, Numbers[D])
#     D -= 2


# 0 Null 9 Nine
# 1 One  8 Eight
#D = 0
#C = len(Numbers) - 1
#while (D < len(Numbers)):
#     print(D, Numbers[D], C, Numbers[C])
#     D += 1
#     C -= 1

#D = 0
#L = len(Numbers) - 1 
#while (D < len(Numbers)):
     #print(D, L-D)
     #print(Numbers[D],'-',Numbers[L-D])
     #print(Numbers[D] + '-' + Numbers[L-D])
 #    print('%s-%s' % (Numbers[D], Numbers[L-D]))
 #    D += 1


D = 0
L = len(Numbers) - 1 
while (D <= L):
     #print(str(D) + '+' + str(L-D) + '=' + str(D+L-D))
     print('%s+%s=%s' %(D, L-D, D+(L-D)))
     D += 1

print('The end')