import time
import datetime


class TPerson():
    def __init__(self): 
        self.Name: str = ''
        self.Age: int  = 0
        self.Male: bool = None
        self.Height: int = 0
        self.Weight: int = 0
        self.Friends: list = []

        #ToDo
        #BirthDay

    def Init(self, aName: str, aAge: int, aMale: bool, aHeight: int, aWeight: int):
        self.Name = aName
        self.Age = aAge
        self.Male = aMale
        self.Height = aHeight
        self.Weight = aWeight

    def AddFriend(self, aPerson: 'TPerson'):
        print('Adding a friend %s for %s' % (aPerson.Name, self.Name))
        if (self != aPerson):
            if (aPerson not in self.Friends):
                self.Friends.append(aPerson)
                aPerson.Friends.append(self)
                print('УРА МИ ДРУЗІ')
            else:
                print('you are already a friend with %s' % (self.Name))
        else:
            print('You cant be a friend with yourself')
        
    def ShowFriends(self):
        Len = len(self.Friends) 
        if (Len == 0):
            print('You have no friends')
        elif (Len == 1):
            print('Friend: %s' % (Len))
            print('Friend: %s' %  (self.Friends[0].Name))
        else:
            print('Friends: %s' % (Len))
            #for F in self.Friends:
            #    print('Friend: %s' %  (F.Name))

            i = 0
            while(i < Len):
                Person = self.Friends[i]
                print('Friend: %s %s %s' % (Person.Name, Person.Age, Person.Weight))
                i += 1
 
    def Info(self): 
        print('Name   : %s' % (self.Name))
        print('Age    : %s' % (self.Age))
        print('Male   : %s' %  (self.Male))
        print('Height : %s' %  (self.Height))
        print('Weight : %s' %  (self.Weight))
        self.ShowFriends()

    def IsTeenAge(self):
        if (self.Age >= 13) and (self.Age <= 19):
            print('%s Is TeenAger' % (self.Name))
        else:
            print('%s Is Not TeenAger' % (self.Name))


class TStudent(TPerson):
    def __init__(self): 
        super().__init__()

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
    Person1.Male = True
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
    print()
    P1 = TPerson()
    P1.Init('Davyd', 13, True, 180, 50)
    P1.IsTeenAge()
    P1.Info()

    print()
    S1 = TStudent()
    S1.Init('Yaroslav', 21, True, 191, 96)
    S1.School = 'SH-24'
    S1.Class = '11A'

    print()
    P2 = TPerson()
    P2.Init('Dmytro', 14, True, 181, 60)
    P2.IsTeenAge()
    P2.AddFriend(P1)
    P2.AddFriend(P1)    
    P2.AddFriend(P2)    
    P2.AddFriend(S1)    
    P2.Info()

#Test1()
Test2()
