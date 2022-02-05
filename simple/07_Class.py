import time
import datetime


class TPerson():
    def __init__(self): 
        self.Name: str = ''
        self.Age: int  = 0
        self.Male: bool = None
        self.Height: int = 0
        self.Weight: int = 0
        self.Friends = []

        #ToDo
        #BirthDay

    def Init(self, aName: str, aAge: int, aMale: bool, aHeight: int, aWeight: int):
        self.Name = aName
        self.Age = aAge
        self.Male = aMale
        self.Height = aHeight
        self.Weight = aWeight

    def AddFriend(self, aPerson: 'TPerson'):
        if (not aPerson in self.Friends):
            self.Friends.append(aPerson)
            aPerson.Friends.append(self)
        else:
            print('already friend with ' + aPerson.Name)

    #ToDo
    #def ShowFriends(self):
    #    pass
 
    def Info(self): 
        print('Name: ' +  self.Name)
        print('Age: ' +  str(self.Age))
        print('Male: %s' %  (self.Male))
        print('Height: %s' %  (self.Height))
        print('Weight: %s' %  (self.Weight))

        for Friend in self.Friends:
            print('Friend: %s' %  (Friend.Name))

class TStudent(TPerson):
    def __init__(self): 
        super().__init__()

        self.School: str = ''
        self.Class: str  = ''

    def Info(self): 
        super().Info()
        print('School: %s' %  (self.School))    
        print('Class: %s' %  (self.Class))


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
Student1.AddFriend(Person1)
Student1.Info()

print()
Person1.AddFriend(Student1)
Person1.Info()
