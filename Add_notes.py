import re
from collections import UserList
import pickle


class Note:
    def __init__(self, title, text):
        self._title = title
        self._text = text
        self._tags_dict = {}
        self._parse_tags()

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    @property
    def tags_dict(self):
        return self._tags_dict

    def _parse_tags(self):
        # Регулярний вираз для пошуку хештегів в тексті
        pattern = r"#\w+"
        tags = re.findall(pattern, self._text)

        for tag in tags:
            tag = tag[1:]  # Видаляємо символ "#" з тегу
            self._tags_dict[tag] = self._tags_dict.get(tag, 0) + 1

    @text.setter
    def text(self, new_text):
        self._text = new_text
        self._parse_tags()

class NotesList(UserList):
    def __init__(self):
        super().__init__()
        self.filename = "notes.pkl"  # Назва файлу для збереження нотаток

        # Перевизначення методу append для автоматичного збереження при додаванні нотаток
    def append(self, note):
        super().append(note)
        self._save_notes_to_file()

        # Збереження нотаток у файл
    def _save_notes_to_file(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

        # Завантаження нотаток з файлу
    def load_notes_from_file(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = []

    # Код для збереження та завантаження нотаток
notes_list = NotesList()
notes_list.load_notes_from_file()

note1 = Note("Title 1", "Text of Note 1 #tag1 #tag2")
note2 = Note("Title 2", "Text of Note 2 #tag2 #tag3")
notes_list.append(note1)  # Автоматичне збереження при додаванні
notes_list.append(note2)

# Виведення нотаток
for note in notes_list:
    print(f"Title: {note.title}")
    print(f"Text: {note.text}")
    print(f"Tags: {note.tags_dict}")