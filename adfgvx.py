import sys
from encryption import main

command = sys.argv[1]

if command == 'cripto':
    title = sys.argv[2]
    key = sys.argv[3]
    table_key = sys.argv[4]
    chipher = main(title, 'привет дорогой друг', key, table_key)
    print(chipher)
elif command == 'help':
    pass
