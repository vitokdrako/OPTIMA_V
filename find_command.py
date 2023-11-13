import re


'''Виправляємо введений рядок. Чистимо від всіх символів, окрім літер. 
 Видаляємо повторення літер, якщо вони зустрічаються більше 2 разів підряд'''
def shrink_input(user_input):
    pure_input = re.sub(r'[^a-zA-Z]', '', user_input)
    pure_input = re.sub(r'(.)\1{2,}', r'\1\1', pure_input)
    return pure_input


'''Створюємо новий словник для обробки команд без пробілів'''
def create_dict_of_command(commands):
    return [{i : re.sub('\W|\d', '', i)} for i in commands]


'''Шукаємо повне співпадіння введеного рядку в будь-якій команді'''
def match(pure_input, commands):
    return [k for command in commands for k, v in command.items() if pure_input in v]


'''Шукаємо повне співпадіння введеного рядку, якщо неправильний порядок введних символів'''
def match_mixed_letters(pure_input, commands):
    return [k for command in commands for k, v in command.items() if sorted(pure_input) == sorted(v)]


'''Заміняємо кожний символ на .?(будь-який символ 0 або 1 раз), для пошуку однієї помилки у слові'''
def regexed_input_one_d(pure_input, ind):
    return pure_input[:ind] + '.?' + pure_input[ind + 1:]


'''Пошук однієї помилки у слові'''
def one_dimensional(pure_input, commands):
    list_of_possible_commands = []
    for command in commands:
        for k, v in command.items():
            if any(re.findall(regexed_input_one_d(pure_input, ind), v) for ind in range(len(pure_input))):
                list_of_possible_commands.append(k)
    return list_of_possible_commands


'''Заміна двох симолів у слові на .?(будь-який символ 0 або 1 раз) та .* (будь-який символ 0 або більше разів)'''
def regexed_input_two_d(pure_input, fixed_ind, ind):
    temp_list = list(pure_input)
    temp_list[fixed_ind] = '.?'
    temp_list[ind]='.*'
    return ''.join(temp_list)


'''Пошук більше двох помилок у слові (скільки точно не доганяю, але думаю не більше 3)'''
def two_dimensional(pure_input, len_of_input, commands):
    list_of_possible_commands = []
    for counter in range(len_of_input):
        for command in commands:
            for k_command, v_command in command.items():
                for ind, _ in enumerate(pure_input):
                    re_symbol = regexed_input_two_d(pure_input, counter, ind)
                    result = re.findall(re_symbol, v_command)
                    if result and k_command not in list_of_possible_commands:
                        list_of_possible_commands.append(k_command)
    return list_of_possible_commands


'''Додатковий інпут для уточення, якщо знайдено одне співпадіння'''
def find_one_command(processed_input, commands):
    new_input = input(f'Did you mean command: <{processed_input}> ? Y/N: ')
    if new_input.lower() == 'Y'.lower():
        for command in commands:
            if processed_input in command:
                return processed_input
    return new_input

'''Додатковий інпут для уточення, якщо більше одного співпадіння'''
def choose_command(processed_input):
    dict_of_possible_commands ={}
    print ('Did you mean one of the following commands?')
    for k, v in enumerate(processed_input):
        dict_of_possible_commands[k+1] = v
        print(k + 1, v)    
    new_input = input(f'Choose number of command or press any key to continue: ')
    try:
        new_input = int(new_input)
        if new_input == 1:
            return dict_of_possible_commands[new_input]
        return 'value out of sequence'
    except:
        return new_input
    

'''Основна функція'''
def get_command(user_input, list_of_commands):
    possible_command=''
    pure_input = shrink_input(user_input)
    len_of_input = len(pure_input)
    
    if len_of_input < 3:
        return user_input
    
    commands = create_dict_of_command(list_of_commands)
    list_of_possible_commands = match(pure_input, commands)
    
    if not list_of_possible_commands:
        list_of_possible_commands = match_mixed_letters(pure_input, commands)    
    if not list_of_possible_commands:
        list_of_possible_commands = one_dimensional(pure_input, commands)
    if not list_of_possible_commands:      
        if len_of_input>=5:
            list_of_possible_commands = two_dimensional(pure_input, len_of_input, commands)
    
    if len(list_of_possible_commands) == 1:
        possible_command = find_one_command(list_of_possible_commands[0], commands)
    if len(list_of_possible_commands) > 1:
        possible_command = choose_command(list_of_possible_commands)
    
    return possible_command if possible_command else user_input


if __name__=='__main__':
    list_of_commands = ['help', 'hello', 'add contact', 'delete contact', 'edit contact', 'phone', 'address', 
                'birthday', 'email', 'search contacts', 'show contacts', 'show birthdays', 'add note', 
                'delete note', 'edit note', 'search note', 'search note tag', 'show notes', 'sort tag', 
                'sort files', 'good bye', 'close', 'exit', 'stop']  
    while True:
        user_input = input('Enter your command: ')
        if user_input not in list_of_commands:
            #заходити в пошук тільки якщо введено більше 3 букв
            result = get_command(user_input, list_of_commands)
            print (result)
            # if len(result) == 1:
            #     print(f'Did you mean command: {result[0]} ?')
            # elif len(result) > 1:
            #     print(f'Did you mean one of the following commands?')
            #     for k, v in enumerate(result):
            #         print(k + 1, v)
            # else:
            #     print('Command not found. Try again.')
        else:
            print (f'your command is {user_input}')

        if user_input in ('good bye', 'close', 'exit', 'stop'):
            break    