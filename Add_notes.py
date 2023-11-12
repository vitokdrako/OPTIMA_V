"""
- Під капотом тегів - словник, де ключ - текст тегу, в видрук іде тільки перелік ключів
- Теги лишаються в тексті нотатки, але дублюються в поле тегів без знаку #
- Повернула функцію def _parse_tags та оголошення notes_list, бо без нього не працює корректно
"""


import re
from collections import UserList
import pickle


class Note:
    def __init__(self, title: str, text: str) -> None:
        self._title = title
        self._text = text
        self._tags_dict = {}
        self._parse_tags()

    def __str__(self) -> str:
        #num = notes_list.index(note)+1
        tags = ', '.join(tag for tag in self._tags_dict.keys())
        return "{:<20} {:<20} {:<50}".format(self.title, tags, self.text)

    @property
    def title(self) -> str:
        return self._title

    @property
    def text(self)  -> str:
        return self._text

    @property
    def tags_dict(self) -> dict:
        return self._tags_dict

    def _parse_tags(self) -> None:
        pattern = r"#\w+"
        tags = re.findall(pattern, self._text)
    
        for tag in tags:
            tag = tag[1:]
            self._tags_dict[tag] = self._tags_dict.get(tag, 0) + 1




    @text.setter
    def text(self, new_text: str) -> None:
        self._text = new_text
        self._parse_tags()


class NotesList(UserList):
    def __init__(self) -> None:
        super().__init__()
        self.filename = "notes.bin"
        self.load_notes_from_file()

    def append(self, note) -> None:
        super().append(note)
        self._save_notes_to_file()

    def remove(self, num: int) -> None:
        self.data.pop(num-1)
        self._save_notes_to_file()

    def edit(self, num: int, title: str, text: str) -> None:
        note = Note(title, text)
        self.data[num-1] = note
        self._save_notes_to_file()

    def _save_notes_to_file(self) -> None:
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_notes_from_file(self) -> None:
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = []
    
    def output_notes(self):
        output = []
        output.append("{:<5} {:<20} {:<20} {:<50}".format("num", "title", "tags", "text"))
        output += list(map(lambda note: f"{(self.data.index(note)+1):<5} {str(note)}" , self.data))
        return output