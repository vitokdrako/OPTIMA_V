import unittest
from datetime import datetime, timedelta
from Address_book import AddressBook, Record

class TestAddressBook(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook("test_file.pkl")

    def tearDown(self):
        self.address_book.__exit__(None, None, None)

    def test_contacts_upcoming_birthdays(self):
        # Додаємо контакти з майбутніми та минулими днями народження
        future_birthday_record = Record("Future Birthday", birthday="15-11-2023")
        past_birthday_record = Record("Past Birthday", birthday="01-01-2000")

        self.address_book.add_record(future_birthday_record)
        self.address_book.add_record(past_birthday_record)

        # Отримуємо список контактів з майбутніми днями народження
        upcoming_birthdays = self.address_book.contacts_upcoming_birthdays(n=7)

        # Перевіряємо, чи майбутній день народження є у списку
        self.assertIn(future_birthday_record, upcoming_birthdays)

        # Перевіряємо, чи минулий день народження відсутній у списку
        self.assertNotIn(past_birthday_record, upcoming_birthdays)

if __name__ == "__main__":
    unittest.main()