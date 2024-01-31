from abc import ABC, abstractmethod

class View(ABC):
    @abstractmethod
    def display(self, data):
        pass

class ConsoleContactView(View):
    def display(self, data):
        for contact in data:
            print(f"Ім'я: {contact.name}, Телефон: {contact.phone}, Електронна пошта: {contact.email}")

class ConsoleNotesView(View):
    def display(self, data):
        for note in data:
            print(f"Нотатка: {note.content}, Дата: {note.date}")

class ConsoleCommandInfoView(View):
    def display(self, data):
        print("Доступні команди:")
        for command in data:
            print(f"Команда: {command.name}, Опис: {command.description}")

def show_contacts(contacts):
    view = ConsoleContactView()
    view.display(contacts)

def show_notes(notes):
    view = ConsoleNotesView()
    view.display(notes)

def show_commands(commands):
    view = ConsoleCommandInfoView()
    view.display(commands)
