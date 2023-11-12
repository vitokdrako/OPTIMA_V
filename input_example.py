from find_command import get_command


commands = ['help', 'hello', 'address', 'add', 'change', 'phone', 'search', 'birthday', 'email', 
            'show all', 'show birthdays', 'delete', 'good bye', 'close', 'exit', 'stop']


while True:
    user_input = input('Enter your command: ')
    if user_input not in commands:
        #заходити в пошук тільки якщо введено більше 3 букв
        result = get_command(user_input, commands)
        if len(result) == 1 and isinstance(result, list):
            print(f'Did you mean command: {result[0]} ?')
        elif len(result) > 1 and isinstance(result, list):
            print(f'Did you mean one of the following commands?')
            for k, v in enumerate(result):
                print(k + 1, v)
        else:
            print('Command not found. Try again.')
    else:
        print (f'your command is {user_input}')

    if user_input in ('good bye', 'close', 'exit', 'stop'):
        break