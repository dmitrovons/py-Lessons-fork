import time
import datetime


'''
#ToDo
#self.BirthDay = datetime.date(2019, 12, 4)
#date.weekday()

Now = datetime.datetime.now()
BirthDay = datetime.date(1971, 8, 19)
Date1 = datetime.date(Now.year, BirthDay.month, BirthDay.day)
Date2 = datetime.date(Now.year, Now.month, Now.day)
print(Date1 - Date2)

class TEnimal():
    def __init__(self): 
        self.Name: str = ''
        self.Age: int  = 0
        self.Gender: bool = None
        self.Height: int = 0
        self.Weight: int = 0
'''

class TPerson():
    def __init__(self, aName: str, aGender: bool):
        self.Name: str = aName
        self.Gender: bool = aGender

        #self.BirthDay = None
        self.Age: int  = 0
        self.Height: int = 0
        self.Weight: int = 0
        self.Friends: list = []
        self.Kids: list = []
        self.Family = None
        self.Father = None
        self.Mother = None

    def Init(self, aAge: int, aHeight: int, aWeight: int):
        self.Age = aAge
        self.Height = aHeight
        self.Weight = aWeight

    def AddKid(self, aPerson: 'TPerson'):
        print('Adding a kid %s for %s ' % (aPerson.Name, self.Name))
        if (self != aPerson):
            if (aPerson not in self.Kids):
                self.Kids.append(aPerson)
                aPerson.Father = self
            else:
                print('%s has already father %s' % (aPerson.Name, self.Name))
        else:
            print('Hey %s! You cant be a father with yourself' % (self.Name))

        
    def AddFriend(self, aPerson: 'TPerson'):
        print('Adding a friend %s (%s) for %s (%s)' % (aPerson.Name, aPerson.Age, self.Name, self.Age))
        if (self != aPerson):
            if (not aPerson in self.Friends):
                self.Friends.append(aPerson)
                aPerson.Friends.append(self)
                print('УРА МИ ДРУЗІ')
            else:
                print('%s is already a friend with %s' % (aPerson.Name, self.Name))
        else:
            print('Hey %s! You cant be a friend with yourself' % (self.Name))

    def ShowFriends(self):
        Len = len(self.Friends) 
        if (Len == 0):
            print('You have no friends')
        elif (Len == 1):
            print('Friend: %s' % (Len))
            print('Friend: %s' %  (self.Friends[0].Name))
        else:
            print('Friends: %s' % (Len))

            #i = 0
            #while(i < Len):
            #    Person = self.Friends[i]
            #    print('Friend: %s %s %s' % (Person.Name, Person.Age, Person.Weight))
            #    i += 1

            for F in self.Friends:
                print('Friend: %s %s %s' % (F.Name, F.Age, F.Weight))

    def MarryA(self, aPerson: 'TPerson'):
        print ('%s and %s are going to be maried' % (self.Name, aPerson.Name))
        # Mary with friend
        if (self != aPerson):
            if (self.Gender != aPerson.Gender):
                if (self.Family != aPerson):
                    if (self in aPerson.Friends) and (aPerson in self.Friends):
                        #if (self.Age >= 18) and (aPerson.Age >= 18):
                        if (self.IsAdult()) and (aPerson.IsAdult()):
                            if (self.Family == None):
                                self.Family = aPerson
                                aPerson.Family = self
                            else:
                                print('%s is married with %s. Cant divorce' % (self.Name, aPerson.Name))
                    else:
                        print('%s is not a friend to %s' % (self.Name, aPerson.Name))
                else:
                    print('%s is meried with %s' % (self.Name, aPerson.Name))               
            else:
                    print('%s is too young. Only %s years' % (self.Name, self.Age))
        else:
            print('%s has same state as %s ! Cant marry' % (self.Name, aPerson.Name))

    def MarryB(self, aPerson: 'TPerson') -> bool:
        print ('%s and %s are going to be maried' % (self.Name, aPerson.Name))

        if (self == aPerson):
            print('%s, You cant marry with yourself' % (self.Name))
            return False

        if (self.Gender == aPerson.Gender):
            print('%s has same state as %s ! Cant marry' % (self.Name, aPerson.Name))                
            return False

        if (self.Family == aPerson):
            print('%s is meried with %s' % (self.Name, aPerson.Name))
            return False

        if (not self in aPerson.Friends) and (not aPerson in self.Friends):
            print('%s is not a friend to %s' % (self.Name, aPerson.Name))
            return False

        if (self.IsAdult()) and (aPerson.IsAdult()):
            print('%s is not a friend to %s' % (self.Name, aPerson.Name))
            return False
        
        if (self.Family != None):
            print('%s is married with %s. Cant divorce' % (self.Name, aPerson.Name))
            return False

        self.Family = aPerson
        aPerson.Family = self
        return True

    def Marry(self, aPerson: 'TPerson'):
        #self.MarryA(aPerson)
        self.MarryB(aPerson)

    def IsAdult(self):
        # ToDo
        if (self.Age >= 18):
            return True
        else:
            return False    

    def GetAge(self):
        pass
 
    def Info(self): 
        print()
        print('Name   : %s' % (self.Name))
        print('Age    : %s' % (self.Age))
        print('Gender : %s' %  (self.Gender))
        print('Height : %s' %  (self.Height))
        print('Weight : %s' %  (self.Weight))

        if (self.Father != None):
            print('Father : %s' %  (self.Father.Name))

        if (self.Family != None):
            print('Family : %s' %  (self.Family.Name))

        self.ShowFriends()


    def IsTeenAge(self):
        if (self.Age >= 13) and (self.Age <= 19):
            print('%s Is TeenAger' % (self.Name))
        else:
            print('%s Is Not TeenAger' % (self.Name))


class TStudent(TPerson):
    def __init__(self, aName: str, aGender: bool): 
        super().__init__(aName, aGender)

        self.School: str = ''
        self.Class: str  = ''

    def Info(self): 
        super().Info()
        print('School: %s' %  (self.School))    
        print('Class: %s' %  (self.Class))


def Test1():
    Person1 = TPerson()
    Person1.Name = 'Davyd'
    Person1.Age = 13
    Person1.Gender = True
    Person1.Height = 180
    Person1.Weight = 50
    Person1.Info()

    print()
    Person2 = TPerson()
    Person2.Init('Dmytro', 14, True, 181, 60)
    Person2.Info()

    print()
    Student1 = TStudent()
    Student1.Init('Yaroslav', 21, True, 191, 96)
    Student1.School = 'SH-24'
    Student1.Class = '11A'
    Student1.Add    #def IsTeenAge

    print()
    Person1.AddFriend(Student1)
    Person1.Info()


def Test2():
    Davyd = TPerson('Davyd', True)
    Davyd.Init(13,  180, 50)

    Yaroslav = TStudent('Yaroslav', True)
    Yaroslav.Init(21, 191, 96)
    Yaroslav.School = 'SH-24'
    Yaroslav.Class = '11A'

    Dmytro = TPerson('Dmytro', True)
    Dmytro.Init(14, 181, 60)
    Dmytro.AddFriend(Davyd)
    Dmytro.AddFriend(Davyd)    
    Dmytro.AddFriend(Dmytro)    
    Dmytro.AddFriend(Yaroslav)    

    Ganna = TPerson('Ganna', False)
    Ganna.Init(20, 165, 50)
    Yaroslav.AddFriend(Ganna)
    Yaroslav.Marry(Ganna)
    Ganna.Marry(Yaroslav)
    Ganna.Marry(Yaroslav)    
    Ganna.Info()

    Vlad = TPerson('Vlad', True)
    Vlad.Init(50, 184, 85)
    Vlad.AddKid(Davyd)

    Davyd.Info()

    print()
    Persons = [Davyd, Yaroslav, Dmytro, Ganna, Vlad]
    for Person in Persons:
       print(Person.Name)

    #print()
    #i = 0
    #while (i < len(Persons)):
    #    Person = Persons[i]
    #    print(Person.Name)
    #    i += 1


#Test1()
Test2()


