#!/usr/bin/python3 -B

'''
Python lesson
Simple dictionary
VladVons@gmail.com, 2022.02.01
'''

import os
import random


class TSimpleDict():
    def __init__(self):                                         # конструктор класу викликається один раз при створенні класу
        self._Clear()

    def _Error(self, aMsg: str):                                # якщо процедура починається з підкреслення, то вона не видима за межами класу
        print('Error. ' + aMsg)                                 # повідомлення помилки
        self.ErrCnt += 1                                        # збільшуєм лічильник помилок на 1

    def _Find(self, aFind: str) -> str:
        aFind = aFind.lower()                                   # перевести в малу букву
        Word = self.Dict.get(aFind, '')                         # отримати значення по ключу, а якщо не знайдено то ''
        return Word

    def _Clear(self):
        self.ErrCnt = 0
        self.Dict1 = {}                                         # створення порожнього словника Eng
        self.Dict2 = {}                                         # створення порожнього словника Ukr
        self.SetDict(True)                                      # встановити словник за замовчуванням Eng

    def _GetRand(self, aCount: int) -> list:
        Keys = self.Dict.keys()                                 # отримати з словника список ключів
        Count = min(aCount, len(Keys))                          # обмежити кількість слів до розміру словника
        return random.sample(Keys, Count)                       # перемішати випадковим чином і вибрати потрібну кількість

    def Info(self):
        print('Simple dictionary class, v1.01, 2022.02.01')
        print('Current directory: ' + os.getcwd())
        print('Words: %d' % (self.GetSize()))

    def SetDict(self, aMode: bool):
        if (aMode):                                             # якщо істина, то встановлює основним словником англ, інакше укр
            self.Dict = self.Dict1
        else:
            self.Dict = self.Dict2

    def GetSize(self) -> int:
        return len(self.Dict1)

    def SetWord(self, aKey: str, aValue: str):
        Key = aKey.strip()                                      # очистити від пробілів
        Value = aValue.strip()
        if (Key == '') or (Value == ''):                        # значення Key або Value не можуть бути порожні
            Msg = 'Key or Value is empty: %s=%s' % (Key, Value)
            self._Error(Msg)
        else:
            if (self.Dict1.get(Key)):
                print('Word exists: ' + Key)

            self.Dict1[Key] = Value                             # записати в словник прямий ключ і значення Dict1['null'] = 'ноль'
            self.Dict2[Value] = Key                             # записати в словник зворотній ключ і значення Dict2['ноль'] = 'null'

    def Show(self, aWord: str):                                 # показати переклад
        Translate = self._Find(aWord)
        if (Translate == ''):
            Translate = 'NOT FOUND'
        print('%s -> %s' % (aWord, Translate))                  # вивести на екран що шукали і переклад

    def ShowAll(self):                                          # вивести всі слова просортовано
        for Key, Value in self.Dict.items():                    # проходимо всі слова
            print('%10s = %s' % (Key, Value))

    def Save(self, aFileName: str, aSort = True):               # записати просортовано у файл
        Words = self.Dict.items()
        if (aSort):
            Words = sorted(Words)                               # сортування

        with open(aFileName, 'w') as hFile:                     # відкрити файл для запису в змінну hFile
            for Key, Value in Words:                            # проходимо всі слова
                hFile.write('%s = %s\n' % (Key, Value))         # запис кожної пари слів

    def Load(self, aFileName: str):                             # self вказуэ на клас
        self._Clear()

        with open(aFileName, 'r') as hFile:                 # відкрити файл для читання в змінну hFile
            for LineNo, Line in enumerate(hFile):               # завантажити в циклі по одній стрічці з файлу в змінну Line. 'Null = Ноль '
                Line = Line.strip().lower()                     # очистити від пробілів 'Null=Ноль' і перевести в малу букву 'null=ноль'
                if (Line == '') or (Line.startswith('#')):      # перевірити чи стрічка пуста і закоментована
                    continue                                    # на початок циклу

                Arr = Line.split('=')                           # розбити стрічку на дві частини за роздільником '=' ['null', 'ноль ']
                if (len(Arr) == 2):                             # перевірити чи є дві частини
                    # Key = Arr[0]                              # отримати значення з масиву. Спосіб 1
                    # Value = Arr[1]
                    Key, Value = Arr                            # отримати значення з масиву. Спосіб 2. Буде Key = null', value = 'ноль'
                    self.SetWord(Key, Value)
                else:
                    Msg = 'Line %s. Line must have two parts "%s"' % (LineNo + 1, Line)
                    self._Error(Msg)

        if (self.ErrCnt > 0):                                   # якщо є помилки то інформуємо
            print('Errors: %d' % (self.ErrCnt))



class TLearnDict(TSimpleDict):
    def ShowRand(self, aCount: int):
        Keys = self._GetRand(aCount)                            # отримати список випадкових слів
        for Key in Keys:                                        # вивести на акран
            print('%10s = %s' % (Key, self.Dict[Key])) 

    def Learn(self, aTips: int = 5, aCount: int = 10):
        Praise = ['good', 'ok', 'nice', 'super', 'best', 'wow', 'bravo', 'smart', 'clever', 'amazing', 'well', 'cool', 'beautiful', 'cute', 'charm', 'glamour', 'graceful', 'elegant']

        SDictErr = TSimpleDict()
        aTips = min(len(self.Dict), aTips)
        Score = 0
        self.ErrCnt = 0

        for Count in range(aCount):
            Keys = self._GetRand(aTips)

            if (SDictErr.GetSize() > 0):
                KeyErr = SDictErr._GetRand(1)[0]
                Rand = random.randint(0, aTips - 1)
                Keys[Rand] = KeyErr

            Rand = random.randint(0, aTips - 1)
            RandKey = Keys[Rand]
            RandValue = self._Find(RandKey)

            print()
            print('-= %3d/%3d, Score: %d, Errors: %d =-' % (Count+1, aCount, Score, self.ErrCnt))
            for Idx, Key in enumerate(Keys):
                print(Idx + 1, Key)

            Answer = input('%s: ' % (RandValue))
            if (Answer.isdigit()):
                Answer = int(Answer)
                if (Answer <= aTips):
                    if (Answer - 1 == Rand):
                        Score += 1
                        print('%s. %s!' % (RandKey, Praise[random.randint(0, len(Praise) - 1)]))
                    else:
                        Msg = '%s = %s' % (RandValue, RandKey)
                        self._Error(Msg)

                        SDictErr.SetWord(RandKey, RandValue)

                        Score -= 3
                        if (Score < -10):
                            break
        print('\nGame over !')

        if (SDictErr.GetSize() > 0):
            print('Your faults:')
            SDictErr.ShowAll()
        else:
            print('You have no errors !')



def Test():
    Dict = TSimpleDict()                                       # створити клас і виклик його __init__()
    Dict.Load('test.dic')

    print()
    print('eng-ukr:')
    Dict.Show('three')                                         # переклад 2. одного слова
    Dict.Show('boy')
    Dict.Show('dog')

    print()
    print('Adding dog = собака')
    Dict.SetWord('dog', 'собака')

    Dict.SetDict(False)                                        # встановити укр словник

    print()
    print('ukr-eng:')
    Words = ['три', 'хлопець', 'собака']                        # переклад 3. списку слів
    for Word in Words:
        Dict.Show(Word)

    print()
    print('All words sorted:')
    Dict.ShowAll()                                             # показати просортований і очищений словник

    print()
    print('Create sorted dictionary file:')
    Dict.Save('test_sorted.dic')                                                # зберегти у файл просортований і очищений словник


def Learn():
    Dict = TLearnDict()
    Dict.Load('eng-ukr.dic')

    print()
    Dict.Info()

    Mode = bool(random.getrandbits(1))
    Dict.SetDict(Mode)

    print('Random words:')
    Dict.ShowRand(10)

    print()
    Dict.Learn()

#Test()
Learn()
