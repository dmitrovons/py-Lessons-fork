'''
simple dictionary
2022.02.01

---

словник в пітоні:
DigitDictSample = {'Null': 'Ноль', 'One': 'Один', 'Two': 'Два', 'Three': 'Три', 'Four': 'Чотири', 'Five': 'Пять', 'Six': 'Шість', 'Seven': 'Сім', 'Eight': 'Вісім', 'Nine': 'Девять'}

---

функції пітона:
open() відкрити файл
split() розбити стрічку за роздільником
strip() обрізати пробіли
lower() перевести стрічку в нижній регістр

---
результат:
Simple dictionary class, v1.01, 2022.02.01
Error. Line 1. Line must have two parts "Smile"
Error. Line 2. Key or Value is empty: smile=
Errors: 2
Words in dictionary: 12

Not good method:
bad -> поганий

Eng-Ukr:
three -> три
boy -> хлопець
dog -> not found

Ukr-Eng:
три -> three
хлопець -> boy
собака -> not found

All words sorted Eng:
       bad = поганий
       boy = хлопець
      five = пять
      four = чотири
      girl = дівчина
      null = ноль
       one = один
     seven = сім
       six = шість
     three = три
      town = місто
       two = два

All words sorted Ukr:
       два = two
   дівчина = girl
     місто = town
      ноль = null
      один = one
   поганий = bad
      пять = five
       сім = seven
       три = three
   хлопець = boy
    чотири = four
     шість = six
'''


class TSimpleDict():
    def __init__(self, aFileName: str):         # конструктор класу викликається один раз при створенні класу
        self.FileName = aFileName               # запамятати назву файлу

        print('Simple dictionary class, v1.01, 2022.02.01')
        self.Load()

    def _Error(self, aMsg: str):
        print('Error. ' + aMsg)                 # повідомлення помилки
        self.ErrCnt += 1                        # збільшуєм лічильник помилок

    def _Find(self, aFind: str, aDict: dict):           # якщо процедура починається з підкреслення, то вона не видима за межами класу
        if (len(aDict) > 0):                            # перевірка чи словник не порожній. Або if (aDict)
            aFind = aFind.lower()                       # перевести в малу букву
            Word = aDict.get(aFind, 'not found')        # отримати значення по ключу, а якщо не знайдено то 'not found'
            print('%s -> %s' % (aFind, Word))           # вивести на екран що шукали і переклад
        else:
            print('dictionary is empty')

    def _GetDict(self, aMode: bool) -> dict:
        if (aMode):
            return self.Dict1
        else:
            return self.Dict2
 
    def Show(self, aMode: bool = True):                 # вивести всі слова просортовано
        Dict = self._GetDict(aMode)
        Words = sorted(Dict.items())
        for Key, Value in Words:
            print('%10s = %s' % (Key, Value))

    def Load(self):                             # self вказуэ на клас
        self.Dict1 = {}                         # створення порожнього словника Eng
        self.Dict2 = {}                         # створення порожнього словника Ukr
        self.ErrCnt = 0                         # очищаємо лічильник помилок

        with open(self.FileName, 'r') as hFile:     # відкрити файл для читання в змінну hFile
            for LineNo, Line in enumerate(hFile):   # завантажити в циклі по одній стрічці з файлу в змінну Line. 'Null = Ноль '
                Line = Line.strip()                 # очистити від пробілів 'Null=Ноль'
                if (Line != ''):                    # перевірити чи стрічка не пуста
                    Arr = Line.split('=')           # розбити стрічку на дві частини за роздільником '=' ['Null', 'Ноль ']
                    if (len(Arr) == 2):             # перевірити чи є дві частини
                        Key, Value = Arr            # розділити масив на два зеачення в зміні. Буде Key = Null', Value = 'Ноль'
                        Key = Key.strip().lower()               # очистити від пробілів і перевести в малу букву 'Null'
                        Value = Value.strip().lower()           # очистити від пробілів і перевести в малу букву 'Ноль'
                        if (Key == '') or (Value == ''):        # значення Key або Value не можуть бути порожні
                            Msg = 'Line %s. Key or Value is empty: %s=%s' % (LineNo + 1, Key, Value)
                            self._Error(Msg)
                        else:
                            self.Dict1[Key] = Value      # записати в словник прямий ключ і значення Dict1['Null'] = 'Ноль'
                            self.Dict2[Value] = Key      # записати в словник зворотній ключ і значення Dict2['Ноль'] = 'Null'
                    else:
                        Msg = 'Line %s. Line must have two parts "%s"' % (LineNo + 1, Line)
                        self._Error(Msg)

        if (self.ErrCnt > 0):
            print('Errors: %d' % (self.ErrCnt))

        print('Words in dictionary: ' + str(len(self.Dict1)))

    def FindEng(self, aFind: str):
        self._Find(aFind, self.Dict1)                   # вказуємо англ словник

    def FindUkr(self, aFind: str):
        self._Find(aFind, self.Dict2)                   # вказуємо укр словник

    def Find(self, aFind: str, aMode: bool):
        Dict = self._GetDict(aMode)
        self._Find(aFind, Dict)


def Main():
    File = 'app_dictionary_vlad.txt'
    DictA = TSimpleDict(File)                         # створити клас

    print()
    print('Not good method:')
    DictA._Find('Bad', DictA.Dict1)            # не гарна ідея. Окультуруємось FindEng

    print()
    print('True Eng, False Ukr:')
    DictA.Find('three', True)
    DictA.Find('три', False)

    print()
    print('Eng-Ukr:')
    DictA.FindEng('three')                      # пошук слова
    DictA.FindEng('boy')
    DictA.FindEng('dog')

    print()
    print('Ukr-Eng:')
    Words = ['три', 'хлопець', 'собака']
    for Word in Words:
        DictA.FindUkr(Word)

    print()
    print('All words sorted Eng:')
    DictA.Show()

    print()
    print('All words sorted Ukr:')
    DictA.Show(False)

Main()
