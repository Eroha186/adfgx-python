import random as rd

alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789 '


def create_title(title):
    for chr_vertical in title:
        for chr_horizontal in title:
            yield chr_vertical + chr_horizontal


def crate_table_text(table_key):
    matrix = []
    if table_key:
        matrix = [i for i in alphabet if i not in table_key]
    else:
        matrix = [i for i in alphabet]
        rd.shuffle(matrix)
    return matrix


def generator_matrix(table_key, title='ABCIDEL'):
    table = {}
    table_key = [chr for chr in table_key] if table_key else None
    matrix_text = crate_table_text(table_key)

    for itm in create_title(title):
        if table_key:
            table[table_key.pop(0)] = itm
            continue

        if matrix_text:
            table[matrix_text.pop(0)] = itm

    return table


def text_encryption(title, text, table_key):
    '''
    Encrypting text based on the table provided
    :param title: The title of the algorithm (ADFGVX)
    :param text: The text to encrypt
    :return: Returns an encrypted sequence
    '''
    table = generator_matrix(table_key, title)
    ciphertext = ''
    for i in text:
        ciphertext += table[i]
    return ciphertext


def creating_a_permutation_table(title, text, key, table_key):
    '''
    Creating a permutation table where the keyword is located in the header
    :param title: The title of the algorithm (ADFGVX)
    :param text: The text to encrypt
    :param key: The key for permutation
    :return: Returns a table with the key header
    '''
    ciphertext = text_encryption(title, text, table_key)
    result = {}
    for num, i in enumerate(key * int(len(ciphertext) / len(key))):
        result[i] = result.get(i) + ciphertext[num:num + 1] if result.get(i) else ciphertext[num:num + 1]
    return result


def permutation(key):
    key = [i for i in key]
    rd.shuffle(key)
    return key


def main(title, text, key, table_key=None):
    result_text = creating_a_permutation_table(title, text, key, table_key)
    key = permutation(key)
    text = ''
    for k in key:
        text += result_text.get(k)
    return text
