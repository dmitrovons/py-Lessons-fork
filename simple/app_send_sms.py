'''
Send sms service
v0.01
2022.01.23
'''

def Input():
    PhoneNumber = '+380686418151'
    CountSMS = 1
    Message = 'Hello'

    #PhoneNumber = input('Phone number: ')
    #CountSMS = input('SMS count: ')
    #Message = input('SMS text: ')

    #Send message "XXX" to phone "XXX" X times ?
    #print('Send message "' + Message + '" to phone "' + PhoneNumber + '" ' + str(CountSMS) + ' times ?')
    YN = input('Send message "%s" to phone "%s" %s times y/n ?' % (Message, PhoneNumber, CountSMS))
    if (YN == 'y') or (YN == 'Y'):
        print('okey')
    else:
        print ('sorry')

def SendSMS ():
    pass


Input()

