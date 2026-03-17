"""
Format validation using regular expressions
"""
import re


class FormatValidator(object):
    def __init__(self):
        self.error = None
        self._text_regex = r"[A-Za-z\s]+"
        self._phone_regex = r"\d{9,9}"
        self._email_regex = r"[\w\d]+@[\w\d]+\.[\w\d]+"
        return

    def check_valid_name(self, name: str) -> bool:
        return self.__check_field(name, self._text_regex, "Name")

    def check_valid_surname(self, surname: str) -> bool:
        return self.__check_field(surname, self._text_regex, "Surname")

    def check_valid_phone(self, phone_number: str) -> bool:
        return self.__check_field(phone_number, self._phone_regex, "Phone number")

    def check_valid_email(self, email: str) -> bool:
        if email is None or email == "":
            return True
        return self.__check4regex(pattern=self._email_regex, text=email, checked_field="Email")

    def __check_field(self, field: str, pattern: str, field_name: str) -> bool:
        if self.__check_input(text=field, checked_field=field_name):
            return self.__check4regex(pattern=pattern, text=field, checked_field=field_name)

    def __check_input(self, text: str, checked_field: str) -> bool:
        if text is None:
            self.error = ("{} is None".format(checked_field))
            return False
        elif text == "":
            self.error = ("{} is empty".format(checked_field))
            return False
        return True

    def __check4regex(self, pattern, text, checked_field: str) -> bool:
        if re.match(pattern=pattern, string=text) is None:
            self.error = ("{} error".format(checked_field))
            return False
        return True
