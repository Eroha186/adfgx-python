import random as rd


def generator_matrix():
    """
    Sequence generator
    :return: Returns a random sequence of 36 characters
    """
    matrix = []
    [matrix.append(chr(item)) for item in range(ord('A'), ord('Z') + 1)] and [matrix.append(itm) for itm in range(10)]
    rd.shuffle(matrix)
    return matrix


def create_table(title):
    '''
    Creating the first table
    :param title: The title of the algorithm (ADFGVX)
    :return: A list with the title
    '''
    table = {}
    matrix = generator_matrix()
    for chr_vertical in title:
        for chr_horizontal in title:
            table[matrix.pop()] = chr_vertical + chr_horizontal
    return table


def text_encryption(title, text):
    '''
    Encrypting text based on the table provided
    :param title: The title of the algorithm (ADFGVX)
    :param text: The text to encrypt
    :return: Returns an encrypted sequence
    '''
    table = create_table(title)
    ciphertext = ''
    for i in text:
        ciphertext += table[i]
    return ciphertext


def creating_a_permutation_table(title, text, key):
    '''
    Creating a permutation table where the keyword is located in the header
    :param title: The title of the algorithm (ADFGVX)
    :param text: The text to encrypt
    :param key: The key for permutation
    :return: Returns a table with the key header
    '''
    ciphertext = text_encryption(title, text)
    result = {}
    for num, i in enumerate(key * int(len(ciphertext) / len(key))):
        result[i] = result.get(i) + ciphertext[num:num + 1] if result.get(i) else ciphertext[num:num + 1]
    return result


def permutation(key):
    key = [i for i in key]
    rd.shuffle(key)
    return key


def main(title, text, key):
    result_text = creating_a_permutation_table(title, text, key)
    key = permutation(key)
    text = ''
    for k in key:
        text += result_text.get(k)
    return text


main('ADFGVX', 'POSHLI', 'PRIVET')
