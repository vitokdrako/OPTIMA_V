"""
- Під капотом тегів - словник, де ключ - текст тегу, в видрук іде тільки перелік ключів
- Теги лишаються в тексті нотатки, але дублюються в поле тегів без знаку #
- Повернула функцію def _parse_tags та оголошення notes_list, бо без нього не працює корректно
- Ширина 50 для поля тегів та 30 для назви
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
        tags = ', '.join(tag for tag in self._tags_dict.keys())
        return "{:<20} {:<20} {:<50}".format(self.title, tags, self.text)

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    @property
    def text(self)  -> str:
        return self._text
    
    @text.setter
    def text(self, value: str) -> None:
        self._text = value
        self._parse_tags()

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

    def remove(self, param: str) -> None:
        index = None
        if param.isdigit():
            index = int(param) - 1            
        else:
            for i, note in enumerate(self.data):
                if note.title.lower() == param.lower():
                    index = i
                    break
        if index is not None:                  
            del self.data[index]
            self._save_notes_to_file()
            return True
        return False

    def edit(self, param: str, title:str, text:str) -> bool:
        index = None
        if param.isdigit():
            index = int(param) -1            
        else:
            for i, note in enumerate(self.data):
                if note.title.lower() == param.lower():
                    index = i
                    break
        if index is not None:                     
            note = Note(title, text)
            self.data[index] = note
            self._save_notes_to_file()
            return True
        return False

    def _save_notes_to_file(self) -> None:
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_notes_from_file(self) -> None:
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = []

    def search(self, query):
        matches = []
        for note in self.data:
            if query.lower() in note.text.lower() or query.lower() in note.title.lower():
                matches.append(note)
        return matches
    
    def sort_by_tag_count(self):
        sorted_notes = sorted(self.data, key=lambda note: sum(note.tags_dict.values()), reverse=True)
        return sorted_notes
    
    def search_by_tag(self, tag: str):
        notes = [note for note in self.data if tag in note.tags_dict]
        return sorted(notes, key=lambda note: note.tags_dict[tag], reverse=True)