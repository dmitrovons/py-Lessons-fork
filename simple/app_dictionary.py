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

результат роботи:
three -> три
boy -> хлопець
dog -> not found

три -> three
хлопець -> boy
собака -> not found
'''


class TDict():
    def __init__(self, aFileName: str):             # конструктор класу викликається один раз при створенні класу
        self.FileName: str = aFileName              # запамятати назву файлу
        self.Data: dict = {}                        # створення порожнього словника

    def Load(self, aMode = '->') -> dict:           # self вказуэ на клас
        self.Data = {}                              # створення порожнього словника
        with open(self.FileName, 'r') as hFile:     # відкрити файл для читання в змінну hFile
            for Line in hFile:                      # завантажити в циклі по одній стрічці з файлу 'Null = Ноль '
                Line = Line.strip()                 # очистити від пробілів 'Null=Ноль'
                if (Line != ''):                    # перевірити чи стрічка не пуста
                    Arr = Line.split('=')           # розбити стрічку на дві частини за роздільником ['Null', 'Ноль ']
                    if (len(Arr) == 2):             # перевірити чи є дві частини
                        Key, Value = Arr            # розбити стрічку на дві частини за роздільником ['Null', 'Ноль ']
                        Key = Key.strip().lower()       # очистити від пробілів і перевести в малу букву 'Null'
                        Value = Value.strip().lower()   # очистити від пробілів і перевести в малу букву 'Ноль'
                        if (aMode == '->'):             # англ -> укр
                            self.Data[Key] = Value      # записати в словник ключ і значення self.Data['Null'] = 'Ноль'
                        else:                           # укр -> англ
                            self.Data[Value] = Key      # записати в словник ключ і значення self.Data['Ноль'] = 'Null'
                    else:
                        print('invalid line %s' % (Line))

    def Find(self, aFind: str):                     # self вказуэ на клас
        aFind = aFind.lower()                       # перевести в малу букву
        Word = self.Data.get(aFind, 'not found')    # отримати значення по ключу, а якщо не знайдено то 'not found'
        print('%s -> %s' % (aFind, Word))           # вивести на екран що шукали і переклад


print()
Dict1 = TDict('app_dictionary_vlad.txt')            # створити клас
Dict1.Load('->')                                    # завантажити словник 'зліва на право'
Dict1.Find('three')                                 # пошук слова
Dict1.Find('boy')
Dict1.Find('dog')

print()
Dict2 = TDict('app_dictionary_vlad.txt')
Dict2.Load('<-')                                    # завантажити словник 'зправа на ліво'
Dict2.Find('три')
Dict2.Find('хлопець')
Dict2.Find('собака')
