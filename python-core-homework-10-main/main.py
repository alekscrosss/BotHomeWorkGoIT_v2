from collections import UserDict
import re
from datetime import datetime
import pickle


class Field:
    def __init__(self, value=None):
        self.__value = value
    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, val):
        self.__value = val
    def __str__(self):
        return str(self.__value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value=None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if not re.match(r"^\d{10}$", str(val)):
            raise ValueError("Phone number should have 10 digits")
        self.__value = val

class Birthday(Field):
    @Field.value.setter
    def value(self, val):
        try:
            datetime.strptime(val, "%d-%m-%Y")
            self.__value = val
        except ValueError:
            raise ValueError("Birthday should be in format dd-mm-yyyy")
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today()
            birth_date = datetime.strptime(self.birthday.value, "%d-%m-%Y")
            next_birthday = datetime(today.year, birth_date.month, birth_date.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day)
            return (next_birthday - today).days
        else:
            raise ValueError("Birthday is not set!")

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone number does not exist!")

    def edit_phone(self, old_phone_number, new_phone_number):
        phone = self.find_phone(old_phone_number)
        if phone:
            index = self.phones.index(phone)
            self.phones[index] = Phone(new_phone_number)
        else:
            raise ValueError("Phone number does not exist!")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __iter__(self):
        return iter(self.data.items())

    def iterator(self, n):
        items = list(self.data.items())
        for i in range(0, len(items), n):
            yield items[i:i + n]

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Only Record instances can be added.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(dict(self.data), file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.data = pickle.load(file)

    def search(self, query):
        result = AddressBook()
        pattern = re.compile(query, re.I)

        for name, record in self.data.items():
            if pattern.search(name) or any(pattern.search(phone.value) for phone in record.phones):
                result[name] = record

        return result
