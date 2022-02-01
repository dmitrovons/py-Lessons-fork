'''
simple dictionary
2022.02.01

DigitDict = {'Null': 'Ноль', 'One': 'Один', 'Two': 'Два', 'Three': 'Три', 'Four': 'Чотири', 'Five': 'Пять', 'Six': 'Шість', 'Seven': 'Сім', 'Eight': 'Вісім', 'Nine': 'Девять'}


open() відкрити файл
split() розбити стрічку за роздільником
strip() обрізати пробіли
lower() перевести стрічку в нижній регістр
'''

class TDict():
    def __init__(self, aFileName: str):             # конструктор класу
        self.FileName: str = aFileName              # запамятати назву файлу
        Data: dict = {}                             # створення порожнього словника

    def Load(self, aMode = '->') -> dict:
        self.Data = {}                              # створення порожнього словника
        with open(self.FileName, 'r') as hFile:     # відкрити файл для читання
            for Line in hFile:                      # завантажити стрічку з файла
                Line = Line.strip()                 # очистити від пробілів
                if (Line != ''):                    # перевірити чи стрічка не пуста
                    Key, Value = Line.split('=')    # розбити стрічку на дві частини за роздільником 
                    Key = Key.strip().lower()       # очистити від пробілів і перевести в малу букву
                    Value = Value.strip().lower()   # очистити від пробілів і перевести в малу букву
                    if (aMode == '->'):             # англ -> укр
                        self.Data[Key] = Value      # записати в словник ключ і зхначення
                    else:                           # укр -> англ
                        self.Data[Value] = Key      # записати в словник ключ і зхначення

    def Find(self, aFind: str):
        aFind = aFind.lower()                       # перевести в малу букву
        Word = self.Data.get(aFind, 'not found')    # отримати значення по ключу
        print('%s -> %s' % (aFind, Word))           # вивести на екран


Dict1 = TDict('app_dictionary_vlad.txt')
Dict1.Load('->')
Dict1.Find('three')
Dict1.Find('boy')
Dict1.Find('dog')

print()
Dict2 = TDict('app_dictionary_vlad.txt')
Dict2.Load('<-')
Dict2.Find('три')
Dict2.Find('хлопець')
Dict2.Find('собака')
