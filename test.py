commands = ['help', 'hello', 'address', 'add', 'change', 'phone', 'search', 'birthday', 'email', 
            'show all', 'show birthdays', 'delete', 'good bye', 'close', 'exit', 'stop']


var_input = 'exit'


def match(var_input, commands):
   for i in commands:
      if sorted(var_input) == sorted(i):
         print(i)

match(var_input, commands)