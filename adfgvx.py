import argparse
import random as rd

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
    return table


def text_encryption(title, text, table_key):
    '''
    Функция выполняет шифрование таблици
    :param title: Заголовок таблици (ADFGVX)
    :param text: Текст шифрования
    :return: Возвращает зашифрованный текст по таблице
    '''
    table = generator_table(table_key, title)
    print(table)
    ciphertext = ''
    for i in text:  # Проход по символам текста
        ciphertext += table[i]  # Шифрование одного символа
    return ciphertext


def creating_a_permutation_table(title, text, key, table_key):
    '''
    Creating a permutation table where the keyword is located in the header
    :param title: Заголовок таблици (ADFGVX)
    :param text: Текст шифрования
    :param key: Ключ для выполнения перестановки
    :return: Возвращает тблицу с заголовком ключа (только по горизонтали)
    '''
    ciphertext = text_encryption(title, text, table_key)
    result = {}
    for num, i in enumerate(key * int(len(ciphertext) / len(key))):  # Проход циклом по ключу и нумирация от 0
        result[i] = result.get(i) + ciphertext[num:num + 1] if result.get(i) else ciphertext[
                                                                                  num:num + 1]  # Создание таблици для перестановки
    return result


def permutation(key):
    '''
    Функция выполняет перестановку
    :param key: Ключ для выполнения перестановки
    :return: Возвращает вариант перестановки
    '''
    key = [i for i in key]  # Создание ключа
    rd.shuffle(key)  # Перестановка ключа
    return key


def main(title, text, key, table_key=None):
    '''
    Функция запуска основной программы, выполняет конкатенацию текста сверху вниз по каждому столбцу
    :param title: Заголовок таблици (ADFGVX)
    :param text: Текст шифрования
    :param key: Ключ для выполнения перестановки
    :param table_key: Слово для заполнения таблици
    :return: Возвращает текст таблици
    '''
    result_text = creating_a_permutation_table(title, text, key, table_key)
    key = permutation(key)
    text = ''
    for k in key:
        text += result_text.get(k)
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



parser = argparse.ArgumentParser(description="ADFGVX шифр", usage="Шифрование: python3 adfgvx.py crypt path_file title_table [-t][--title] [-k][--key] | Дешифрование: python3 adfgvx.py crypt path_file_chiphertext title_table [-t][--title] --key")

parser.add_argument("action", help="Аргумент задет режис работы программы crypt/decrypt (шифрование/дешифрование)")
parser.add_argument("path_file", help="Аргумент указывает с какого файла, брать открытый/закрытый текс")
parser.add_argument("title_table", help="Аргумент, который задет заглавье таблице замен")
parser.add_argument("-t", "--title", dest="title", help="Не обязательный параметр, который задает режим шифрования. Если парметр указан, то алфавит в таблицу замен вписывает по порядку следования в алфавите после слова-пароля, а если нет, то таблица заполняется рандомно")
parser.add_argument("-k", "--key", dest="key", help="Не обязательный параметр, который задет ключ перестановки. Если указан, то используется то значение, которое указали, а если не указан, то используется сгенерированный ключ, который записывается в файл key.keys")

try:
    arg = parser.parse_args()
except BaseException:
    parser.print_help()
    exit()    

if arg.action == 'crypt':
    title = arg.title_table
    key = arg.key
    table_key = arg.title
    file_text = arg.path_file
    cipher = main(title, read_file(file_text), key, table_key)

    write_file('encryption.txt', cipher)
    print(cipher)
elif arg.action == 'decrypt': 
    pass
else: 
    print("Такого режима не существует")
    parser.print_help()
