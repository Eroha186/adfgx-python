import sys
from encryption import main, read_file, write_file

command = sys.argv[1]

if command == 'cripto':
    title = sys.argv[2]
    key = sys.argv[3]
    table_key = sys.argv[4]
    file_text = sys.argv[5]
    cipher = main(title, read_file(file_text), key, table_key)

    write_file('encryption.txt', cipher)
    print(cipher)
elif command == 'help':
    pass
