import shlex
from pathlib import Path
from Address_book import AddressBook, Record, DuplicatedPhoneError
from Add_notes import Note, NotesList
from sorting import sort_folders_and_return_result

records: AddressBook = None
notes_list = NotesList()

def input_error(*expected_args):
    def input_error_wrapper(func):
        def inner(*args):
            try:
                return func(*args)
            except IndexError:
                return f"Please enter {' and '.join(expected_args)}"
            except KeyError:
                return f"The record for contact {args[0]} not found. Try another contact or use help."
            except ValueError as error:
                if error.args:
                    return error.args[0]
                return f"Phone format '{args[1]}' is incorrect. Use digits only for phone number."
            except DuplicatedPhoneError as phone_error:
                return f"Phone number {phone_error.args[1]} already exists for contact {phone_error.args[0]}."
            # except AttributeError:
            #     return f"Contact {args[0]} doesn't have birthday yet."
        return inner
    return input_error_wrapper

def capitalize_user_name(func):
    def inner(*args):
        new_args = list(args)
        new_args[0] = new_args[0].title()
        return func(*new_args)
    return inner

def unknown_handler(*args):
    return f"Unknown command. Use <help>"

def help_handler():
    help_txt = ""
    def inner(*args):
        nonlocal help_txt
        if not help_txt:
            with open("help.txt") as file:            
                help_txt = "".join(file.readlines())
        return help_txt
    return inner

@capitalize_user_name
@input_error("name", "phone")
def add_contact_handler(*args):
    user_name = args[0]
    user_phones = args[1:]
    record = records.find(user_name, True)
    if not record:
        record = Record(user_name)
        for user_phone in user_phones:
            record.add_phone(user_phone)
        records.add_record(record)
        if user_phones:
            return f"New record added for {user_name} with phone number{'s' if len(user_phones) > 1 else ''}: {'; '.join(user_phones)}."
        return f"New record added for {user_name}."
    else:
        response = []
        for user_phone in user_phones:
            record.add_phone(user_phone)
            response.append(f"New phone number {user_phone} for contact {user_name} added.")
        return "\n".join(response)

@input_error("title", "text")    
def add_note_handler(*args):
    note_title = args[0] if len(args) > 1 else "Untitled"
    note_text = args[1] if len(args) > 1 else args[0]
    note = Note(note_title, note_text)
    notes_list.append(note)
    return f"New note with title '{note_title}' and text '{note_text}' added."

@capitalize_user_name
@input_error("name", "old_phone", "new_phone")
def edit_contact_handler(*args):
    user_name = args[0]
    old_phone = args[1]
    new_phone = args[2]
    record = records.find(user_name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"Phone number for {user_name} changed from {old_phone} to {new_phone}."

@capitalize_user_name    
@input_error("name")
def birthday_handler(*args):
    user_name = args[0]
    user_birthday = args[1] if len(args) > 1 else None
    record = records.find(user_name)
    if record:
        if user_birthday:
            record.add_birthday(user_birthday)
            return f"Birthday {user_birthday} for contact {user_name} added."
        else:
            return f"{record.days_to_birthday()} days to the next {user_name}'s birthday ({record.birthday})."

@capitalize_user_name    
@input_error("name")        
def address_handler(*args):
    user_name = args[0]
    user_address = args[1] if len(args) > 1 else None
    record = records.find(user_name)
    if record:
        if user_address:
            record.add_address(user_address)
            return f"Address '{user_address}' for contact {user_name} added."
        else:
            return f"Address for contact {user_name}: {record.address}."

@capitalize_user_name    
@input_error("name")        
def email_handler(*args):
    user_name = args[0]
    user_email = args[1] if len(args) > 1 else None
    record = records.find(user_name)
    if record:
        if user_email:
            record.add_email(user_email)
            return f"Email '{user_email}' for contact {user_name} added."
        else:
            return f"Email for contact {user_name}: {record.email}."

@capitalize_user_name    
@input_error("name")
def delete_contact_handler(*args):
    user_name = args[0]
    user_phones = args[1:]
    if len(user_phones) >= 1:
        record = records.find(user_name)
        if record:
            response = []
            for user_phone in user_phones:
                record.remove_phone(user_phone)
                response.append(f"Phone number {user_phone} for contact {user_name} removed.")
            return "\n".join(response)
    else:
        if records.delete(user_name):
            return f"Record for contact {user_name} deleted."
        return f"Record for contact {user_name} not found."

@input_error([])
def greeting_handler(*args):
    greeting = "How can I help you?"
    return greeting

@capitalize_user_name
@input_error("name")
def phone_handler(*args):
    user_name = args[0]
    record = records.find(user_name)
    if record:
        return "; ".join(p.value for p in record.phones)

@input_error("query")
def search_contact_handler(*args):
    query: str = args[0]
    contacts = records.search_contacts(query)
    if contacts:
        return "\n".join(str(contact) for contact in contacts)
    return f"No contacts found for '{query}'."

@input_error("days")
def show_birthdays_handler(*args):
    days = int(args[0])
    contacts = records.contacts_upcoming_birthdays(days)
    if contacts:
        return "\n".join(str(contact) for contact in contacts)
    return f"No contacts have birthdays within following {days} days."

def show_notes_handler(*args):
    return "\n".join(notes_list.output_notes())

@input_error([])
def show_contacts_handler(*args):
    return records.iterator()

@input_error("path")
def sort_files_handler(*args):
    folder_path = args[0]
    result = sort_folders_and_return_result(folder_path)
    return result

@input_error("title or number")
def delete_note_handler(*args):
    param = " ".join(args)
    if notes_list.remove(param):
        return "Note deleted successfully."
    else:
        return "Note with this title not found."

@input_error("old title or number", "new title", "new text")
def edit_note_handler(*args):
    param, new_title, new_text = args[0], args[1], args[2]
    if notes_list.edit(param, new_title, new_text):
        return f"Note '{param}' edited successfully."
    else:
        return f"No notes found by the specified param '{param}'."


@input_error("query")
def search_notes_handler(*args):
    query = args[0]
    matches = notes_list.search(query)
    if matches:
        return "\n".join(map(lambda note: str(note), matches))
    else:
        return f"No notes found for query '{query}'."
    
@input_error("tag")
def search_notes_by_tag_handler(*args):
    tag = args[0]
    matches = notes_list.search_by_tag(tag)
    if matches:
        return "\n".join(map(lambda note: str(note), matches))
    else:
        return f"No notes found with tag '{tag}'."

def sort_notes_by_tag_count_handler():
    sorted_notes = notes_list.sort_by_tag_count()
    if sorted_notes:
        return "\n".join(map(lambda note: str(note), sorted_notes))
    else:
        return "No notes to sort."

COMMANDS = {
            help_handler(): "help",
            greeting_handler: "hello",                        
            add_contact_handler: "add contact",
            delete_contact_handler: "delete contact",
            edit_contact_handler: "edit contact",
            phone_handler: "phone",
            address_handler: "address",            
            birthday_handler: "birthday",
            email_handler: "email",            
            search_contact_handler: "search contact",
            show_contacts_handler: "show contacts",            
            show_birthdays_handler: "show birthdays",            
            add_note_handler: "add note",
            delete_note_handler: "delete note",
            edit_note_handler: "edit note",
            search_notes_handler: "search note",
            search_notes_by_tag_handler: "search note tag",
            show_notes_handler: "show notes",            
            sort_notes_by_tag_count_handler: "tag sort",
            sort_files_handler: "sort files"
            }
EXIT_COMMANDS = {"good bye", "close", "exit", "stop", "g"}

def parser(text: str):
    for func, kw in COMMANDS.items():
        if text.startswith(kw):
            return func, shlex.split(text[len(kw):], posix=False)
    return unknown_handler, []

def main():
    global records
    with AddressBook("address_book.pkl") as book:
        records = book
        while True:
            user_input = input(">>> ").lower()
            if user_input in EXIT_COMMANDS:
                print("Good bye!")
                break
            
            func, data = parser(user_input)
            
            if func == sort_files_handler:
                result = func(*data)
                print(result)
                continue
            
            result = func(*data)
            
            if isinstance(result, str):
                print(result)
            else:
                for i in result:                
                    print("\n".join(i))
                    input("Press enter to show more records")


if __name__ == "__main__":
    main()