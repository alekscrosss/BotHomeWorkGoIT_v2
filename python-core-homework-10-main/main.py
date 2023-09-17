from collections import UserDict
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.match(r"^\d{10}$", str(value)):
            raise ValueError("Phone number should have 10 digits")
        super().__init__(value)

    def __eq__(self, other):
        if isinstance(other, Phone):
            return self.value == other.value
        return False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Only Record instances can be added.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
