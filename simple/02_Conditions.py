import datetime

Sunday = 0

#Today = 0
Today = datetime.datetime.today().weekday()
print('Today is %s' % (Today))

if (Today == Sunday):
    print('Hello Sunday !')
else:
    print('Go to school')

IsSunday = (Today == Sunday)
if (IsSunday):
    print('Hello Sunday !')
else:
    print('Go to school')
