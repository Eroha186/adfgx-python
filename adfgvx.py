import argparse
import random as rd
import json

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя '

def create_title(title) -> str:
    '''
    Данная функция реализует заголовки таблици
    :param title: Заголовок таблици (ADFGVX)
    :return: Возврашает пересечение клеток, например, первая клетка "AA"
    '''
    for chr_vertical in title:
        for chr_horizontal in title:
            yield chr_vertical + chr_horizontal  # Конкатенация горизонтального и вертикального заголовка


def crate_table_text(table_key) -> list:
    '''
    Функция создаёт список из элементов таблици
    :param table_key: Слово для заполнения таблици
    :return: Возвращает упорядоченный список элементов таблици
    '''
    if table_key:  # Если есть ключ, тогда создаём список без элементов ключа
        matrix = [i for i in alphabet if i not in table_key]
    else:  # Иначе заполняем список всеми элементами алфавита
        matrix = [i for i in alphabet]
        rd.shuffle(matrix)  # Перемещиваем упорядоченный список
    return matrix


def generator_table(table_key, title='АБВГДЕ') -> dict:
    '''
    Данная функция создаёт словарь (Таблицу для шифрования)
    :param table_key: Слово для заполнения таблици
    :param title: Заголовок таблици (ADFGVX)
    :return: Возвращает готовую таблицу в виде словаря
    '''
    table = {}
    table_key = [chr for chr in table_key] if table_key else None  # Если есть ключ, тогда создаём список
    matrix_text = crate_table_text(table_key)  # Создание списка значений

    for itm in create_title(title):
        if table_key:  # Если ключ есть в таблице, тогда добавляем его в таблицу
            table[table_key.pop(0)] = itm
            continue

        if matrix_text:  # Если в списке значений есть элементы, тогда добавляем их в таблицу
            table[matrix_text.pop(0)] = itm
    
    # Записываем таблицу для шифрования в файл
    with open("table_for_cipher.json", "w") as write_file:
        json.dump(table, write_file)   
      
    return table


def text_encryption(title, text, table_key):
    '''
    Функция выполняет шифрование таблици
    :param title: Заголовок таблици (ADFGVX)
    :param text: Текст шифрования
    :return: Возвращает зашифрованный текст по таблице
    '''
    table = generator_table(table_key, title)
    ciphertext = ''
    for i in text:  # Проход по символам текста
        ciphertext += table[i]  # Шифрование одного символа
    return ciphertext


def creating_a_permutation_table(title, text, key, table_key):
    '''
    Создание таблицы перестановок, в которой ключевое слово находится в заголовке
    :param title: Заголовок таблици (ADFGVX)
    :param text: Текст шифрования
    :param key: Ключ для выполнения перестановки
    :return: Возвращает таблицу с заголовком ключа (только по горизонтали)
    '''
    ciphertext = text_encryption(title, text, table_key)
    result = {}
    for num, i in enumerate(key * (int(len(ciphertext) / len(key)) + 1)):  # Проход циклом по ключу и нумирация от 0
        result[i] = result.get(i) + ciphertext[num:num + 1] if result.get(i) else ciphertext[
                                                                                  num:num + 1]  # Создание таблици для перестановки
    return result


def sort_key(key):
    '''
    Функция выполняет перестановку
    :param key: Ключ для выполнения перестановки
    :return: Возвращает отсартированный ключ
    '''
    key = sorted([i for i in key])  # Создание ключа
    return key

def transform_text(text):
    '''
    Функция преобразовывает текст в нужную программе форму
    :param text: Шифротекст для преобразования
    :return bigramm: Возвращает биграммы преобразованного текста
    '''
    key_sorted = sort_key(key)    

    # узнаем сколько букв заполнено в последней строке таблице
    remainder = len(text) % len(key)
    
    len_str_slice = {}

    # Создаем словарь, в котором указано какая длинна столбца соответсвует букве из пароля, не учитывая последнюю строку
    for i in key:
        len_str_slice[i] = int(len(text) / len(key))

    # Дополняем словарь с учетом последней строки таблицы
    if remainder > 0:
        for i in range(0, remainder):
            len_str_slice[key[i]] = len_str_slice.get(key[i]) + 1
    
    # Нарезаем текст, востанавливая таблицу перестановок
    num = 0
    sliced_text = {}
    for i in key_sorted:
        sliced_text[i] = text[num: num + len_str_slice[i]]
        num += len_str_slice[i]        

    # Созадем матрицу, в которую записываем буквы по строчно из таблицы перестановок
    arr = {}
    for i in key:
        num = 0
        for j in sliced_text[i]:
            if(arr.get(num) == None):
                arr.update({ num : j })
            else:
                arr[num] += j    
            num += 1

    # Склеиваем текст
    text = ''
    for i in arr:
        text += arr.get(i)       

    return create_bigramm(text)     

def create_bigramm(text):
    '''
    Функция делит строку на биграммы
    :param text: Текст шифрования
    :return: список биграмм
    '''
    j = 0
    bigramm = []
    for i in range(0, int(len(text)/2)):
        bigramm.append(text[j: j+2])
        j += 2
    return bigramm

def crypt(title, text, key, table_key=None):
    '''
    Функция запуска шифрующей программы, выполняет конкатенацию текста сверху вниз по каждому столбцу
    :param title: Заголовок таблицы (ADFGVX)
    :param text: Текст шифрования
    :param key: Ключ для выполнения перестановки
    :param table_key: Слово для заполнения таблицы
    :return: Возвращает текст таблицы
    '''
    result_text = creating_a_permutation_table(title, text, key, table_key)
    key = sort_key(key)
    text = ''
    for k in key:
        text += result_text.get(k)
    return text

def decrypt(title, ciphertext, key):
    '''
    Функция запуска дешифрующей программы, выполняет конкатенацию текста сверху вниз по каждому столбцу
    :param title: Заголовок таблицы (ADFGVX)
    :param text: Текст шифрования
    :param key: Ключ для выполнения перестановки
    :return: Возвращает расшифрованный текст
    '''

    bigramm = transform_text(ciphertext)

    # Открываем и записываем в переменную таблицу замен 
    data = ''
    with open("table_for_cipher.json", "r") as read_file:
        data = json.load(read_file)  

    # Меняем ключи и значения местами
    data_rev = {v:k for k, v in data.items()}      
    text = ''
    for item in bigramm: 
        text += data_rev[item]
    return text

def read_file(file_name):
    '''
    Выполняет чтение файла
    :param file_name: Название файла
    :return: Текст из файла
    '''
    with open(file_name, 'r', encoding='utf-8') as file:
        return ''.join(file.read().splitlines())


def write_file(file_name, text):
    '''
    Выполняет запись текста в файл
    :param file_name: Название файла
    :param text: Текст для записи
    '''
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)

def randomKey():
    '''
    Выполняет рандомную генерацию ключа
    :return: Ключ
    '''
    key = ''
    for x in range(0, rd.randint(5, 15)):
        char = alphabet[rd.randint(0, len(alphabet) - 1)] 
        if char != ' ':
            key += char

    write_file('./key.keys', key)

    return key        

parser = argparse.ArgumentParser(description="ADFGVX шифр", usage="Шифрование: python3 adfgvx.py crypt path_file title_table [-tk][--table_key] [-k][--key] | Дешифрование: python3 adfgvx.py crypt path_file_ciphertext title_table path_file title_table [-tk][--table_key] [-k][--key]")

parser.add_argument("action", help="Аргумент задет режис работы программы crypt/decrypt (шифрование/дешифрование)")
parser.add_argument("path_file", help="Аргумент указывает с какого файла, брать открытый/закрытый текс")
parser.add_argument("title_table", help="Аргумент, который задет заглавье таблице замен")
parser.add_argument("-tk", "--table_key", dest="table_key", help="Не обязательный параметр, который задает режим шифрования. Если парметр указан, то алфавит в таблицу замен вписывает по порядку следования в алфавите после слова-пароля, а если нет, то таблица заполняется рандомно")
parser.add_argument("-k", "--key", dest="key", help="Не обязательный параметр, который задет ключ перестановки. Если указан, то используется то значение, которое указали, а если не указан, то используется сгенерированный ключ, который записывается в файл key.keys")

try:
    arg = parser.parse_args()
except BaseException:
    parser.print_help()
    exit()    

if arg.action == 'crypt':
    title = arg.title_table
    key = arg.key
    if key is None:
        key = randomKey()
    table_key = arg.table_key
    file_text = arg.path_file
    cipher = crypt(title, read_file(file_text), key, table_key)

    write_file('encryption.crypt', cipher)
    print(cipher)
elif arg.action == 'decrypt': 
    title = arg.title_table
    key = arg.key
    if key is None:
        print("Нужен ключ, получить его можно из файла key.keys или использовать ключ, который был использован при шифровании")
        exit()
    file_text = arg.path_file
    open_text = decrypt(title, read_file(file_text), key)   
    print(open_text) 
else: 
    print("Такого режима не существует")
    parser.print_help()
