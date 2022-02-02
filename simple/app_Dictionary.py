'''
Lesson. Simple dictionary
2022.02.01

---

словник в пітоні:
DigitDictSample = {'Null': 'Ноль', 'One': 'Один', 'Two': 'Два', 'Three': 'Три'}

---

функції пітона:
open() відкрити файл
startswith() чи стрічка починається з символа
split() розбити стрічку за роздільником
strip() обрізати пробіли
lower() перевести стрічку в нижній регістр
'''

import os
import random


class TSimpleDict():
    def __init__(self, aFileName: str):                         # конструктор класу викликається один раз при створенні класу
        self.FileName = aFileName                               # запамятати назву файлу

        print('Simple dictionary class, v1.01, 2022.02.01')
        print('Current directory: ' + os.getcwd())

        self.Load()
        self.SetDict(True)                                      # встановити головним англ словник

    def _Error(self, aMsg: str):                                # якщо процедура починається з підкреслення, то вона не видима за межами класу
        print('Error. ' + aMsg)                                 # повідомлення помилки
        self.ErrCnt += 1                                        # збільшуєм лічильник помилок на 1

    def _GetRand(self, aCount: int) -> list:
        Keys = self.Dict.keys()                                 # отримати з словника список ключів
        Count = min(aCount, len(Keys))                          # обмежити кількість слів до розміру словника
        return random.sample(Keys, Count)                       # перемішати випадковим чином і вибрати потрібну кількість

    def _Find(self, aFind: str) -> str:
        aFind = aFind.lower()                                   # перевести в малу букву
        Word = self.Dict.get(aFind, '')                         # отримати значення по ключу, а якщо не знайдено то ''
        return Word

    def SetDict(self, aMode: bool):
        if (aMode):                                             # якщо істина, то встановлює основним словником англ, інакше укр
            self.Dict = self.Dict1
        else:
            self.Dict = self.Dict2

    def SetWord(self, aKey: str, aValue: str):
        Key = aKey.strip()                                      # очистити від пробілів
        Value = aValue.strip()
        if (Key == '') or (Value == ''):                        # значення Key або Value не можуть бути порожні
            Msg = 'Key or Value is empty: %s=%s' % (Key, Value)
            self._Error(Msg)
        else:
            self.Dict1[Key] = Value                             # записати в словник прямий ключ і значення Dict1['null'] = 'ноль'
            self.Dict2[Value] = Key                             # записати в словник зворотній ключ і значення Dict2['ноль'] = 'null'

    def Show(self, aWord: str):                                 # показати переклад
        Translate = self._Find(aWord)
        if (Translate == ''):
            Translate = 'not found'
        print('%s -> %s' % (aWord, Translate))                  # вивести на екран що шукали і переклад

    def ShowAll(self):                                          # вивести всі слова просортовано
        Words = sorted(self.Dict.items())                       # сортування
        for Key, Value in Words:                                # проходимо всі слова
            print('%10s = %s' % (Key, Value))

    def ShowRand(self, aCount: int):
        Keys = self._GetRand(aCount)                            # отримати список випадкових слів
        for Key in Keys:                                        # вивести на акран
            print('%10s = %s' % (Key, self.Dict[Key])) 

    def Save(self, aSort = True):                               # записати просортовано у файл
        Words = self.Dict.items()
        if (aSort):
            Words = sorted(Words)                               # сортування

        FileName = self.FileName + '.dict'                      # додаємо до нового файлу закінчення '.dict'
        print('Creating sorted file ' + FileName)
        with open(FileName, 'w') as hFile:                      # відкрити файл для запису в змінну hFile
            for Key, Value in Words:                            # проходимо всі слова
                hFile.write('%s = %s\n' % (Key, Value))         # запис кожної пари слів

    def Load(self):                                             # self вказуэ на клас
        self.Dict1 = {}                                         # створення порожнього словника Eng
        self.Dict2 = {}                                         # створення порожнього словника Ukr
        self.ErrCnt = 0                                         # очищаємо лічильник помилок

        with open(self.FileName, 'r') as hFile:                 # відкрити файл для читання в змінну hFile
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

        print('Words in dictionary: ' + str(len(self.Dict1)))

    def Learn(self, aCount = 5):
        Praise = ['good', 'ok', 'nice', 'super', 'best', 'wow', 'bravo', 'smart', 'clever']
        aCount = min(len(self.Dict), aCount)
        Score = 0
        Errors = 0
        while True:
            Rand = random.randint(0, aCount - 1)
            Keys = self._GetRand(aCount)
            RandKey = Keys[Rand]
            RandValue = self._Find(RandKey)

            print('\n-= Score: %d, Errors: %d =-' % (Score, Errors))
            for Idx, Key in enumerate(Keys):
                print(Idx + 1, Key)

            Answer = input('%s: ' % (RandValue))
            if (Answer.isdigit()):
                if (int(Answer) - 1 == Rand):
                    Score += 1
                    print('%s. %s !' % (RandKey, Praise[random.randint(0, len(Praise) - 1)]))
                else:
                    print('correct answer: %s = %s' % (RandValue, RandKey))
                    Errors += 1
                    Score -= 3
                    if (Score < -10):
                        print('Game over')
                        break


def Main():
    File = '/home/vladvons/Projects/py/py-Lessons/simple/app_dictionary_vlad.txt'
    DictA = TSimpleDict(File)                                   # створити клас і виклик його __init__()

    print()
    print('Eng-Ukr:')
    DictA.Show('three')                                         # переклад 2. одного слова
    DictA.Show('boy')
    DictA.Show('dog')

    print()
    print('Adding dog = собака')
    DictA.SetWord('dog', 'собака')

    DictA.SetDict(False)                                        # встановити укр словник

    print()
    print('Ukr-Eng:')
    Words = ['три', 'хлопець', 'собака']                        # переклад 3. списку слів
    for Word in Words:
        DictA.Show(Word)

    print()
    print('All words sorted:')
    DictA.ShowAll()                                             # показати просортований і очищений словник

    print()
    print('Random 3 words:')
    DictA.ShowRand(3)

    print()
    print('Create sorted dictionary file:')
    DictA.Save()                                                # зберегти у файл просортований і очищений словник

    DictA.Learn()

Main()
