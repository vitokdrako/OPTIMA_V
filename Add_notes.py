# import re
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

    # irrelevant kode:
    # def _parse_tags(self):
    #     pattern = r"#\w+"
    #     tags = re.findall(pattern, self._text)
    #
    #     for tag in tags:
    #         tag = tag[1:]
    #         self._tags_dict[tag] = self._tags_dict.get(tag, 0) + 1

    @text.setter
    def text(self, new_text):
        self._text = new_text
        self._parse_tags()

    def _parse_tags(self):
        pass


class NotesList(UserList):
    def __init__(self):
        super().__init__()
        self.filename = "notes.pkl"

    def append(self, note):
        super().append(note)
        self._save_notes_to_file()

    def _save_notes_to_file(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_notes_from_file(self):
        try:
            with open(self.filename, 'rb') as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = []
