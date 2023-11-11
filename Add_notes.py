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
        title_str = self._title if self._title is not None else ""
        text_str = self._text if self._text is not None else ""
        return f"Title: {title_str}\nText: {text_str}\nTags: {tags}"

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

    def append(self, note) -> None:
        super().append(note)
        self._save_notes_to_file()

    #def remove(self, num: int) -> None:
       # notes_list.pop(num-1)
       # self._save_notes_to_file()

    def remove_by_title(self, title: str) -> bool:
        for i, note in enumerate(self.data):
            if note.title.lower() == title.lower():
                del self.data[i]
                self._save_notes_to_file()
                return True
        return False

    #def edit(self, num: int, title: str, text: str) -> None:
    
       # note = Note(title, text)
       # notes_list[num-1] = note
       # self._save_notes_to_file()

    def edit_by_title(self, old_title: str, new_title: str, new_text: str) -> bool:
        for note in self.data:
            if note.title.lower() == old_title.lower():
                note.title = new_title
                note.text = new_text
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

notes_list = NotesList()
notes_list.load_notes_from_file()

# Test commands

# note1 = Note("Birthday Party", "John's #birdhday party on Friday")
# notes_list.append(note1)  # Автоматичне збереження при додаванні

# note2 = Note("Purchase list", "Potatoes, bread, milk #buy #food")
# notes_list.append(note2)

# note3 = Note("Bill's B_day", "Dec,12 #birthday #buy_gift")
# notes_list.append(note3)

# notes_list.remove(4)     # видалення нотатки за номером

# notes_list.edit(4, "Mark's birthday", "#buy gift for Mark's #birthday")


# Друк

# print("{:^5} {:<30} {:<50} {:<50}".format("num", "title", "tags", "text"))
# for note in notes_list:
#     print(note)