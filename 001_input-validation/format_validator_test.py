"""
Test for the different values of inputs to the regex validator
"""

import unittest

from format_validator import FormatValidator


# Test Suite in order to organize our tests by groups of functionality
class FormatValidatorTest(unittest.TestSuite):
    class NameTests(unittest.TestCase):  # Tests for Name string
        def test_ShouldPassWhenValidNameFormat(self):
            # given
            name_ok = "Yair SegundoNombre"
            validator = FormatValidator()

            # when
            validator.check_valid_name(name_ok)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldFailWhenEmptyName(self):
            # given
            empty_name = ""
            validator = FormatValidator()

            # when
            validator.check_valid_name(empty_name)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Name is empty", "Not recognized empty name")

        def test_ShouldFailWhenNoneAsName(self):
            # given
            validator = FormatValidator()

            # when
            validator.check_valid_name(None)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Name is None", "Not recognized none name")

        def test_ShouldFailWhenNotValidName(self):
            # given
            ko_name = "_*("
            validator = FormatValidator()

            # when
            validator.check_valid_name(ko_name)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Name error", "Not recognized name error")

    class SurnameTests(unittest.TestCase):  # Tests for Surname string
        def test_ShouldPassWhenValidSurnameFormat(self):
            # given
            surname_ok = "Segura Albarracín"
            validator = FormatValidator()

            # when
            validator.check_valid_surname(surname_ok)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldFailWhenEmptySurname(self):
            # given
            empty_surname = ""
            validator = FormatValidator()

            # when
            validator.check_valid_surname(empty_surname)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Surname is empty", "Not recognized empty surname")

        def test_ShouldFailWhenNoneAsSurname(self):
            # given
            validator = FormatValidator()

            # when
            validator.check_valid_surname(None)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Surname is None", "Not recognized none surname")

        def test_ShouldFailWhenNotValidSurname(self):
            # given
            ko_surname = "_*("
            validator = FormatValidator()

            # when
            validator.check_valid_surname(ko_surname)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Surname error", "Not recognized surname error")

    class PhoneNumberTests(unittest.TestCase):  # Tests for Phone number field
        def test_ShouldPassWhenValidPhoneFormat(self):
            # given
            phone_ok = "912345678"
            validator = FormatValidator()

            # when
            validator.check_valid_phone(phone_ok)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldFailWhenEmptyPhone(self):
            # given
            empty_phone = ""
            validator = FormatValidator()

            # when
            validator.check_valid_phone(empty_phone)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Phone number is empty", "Not recognized empty phone number")

        def test_ShouldFailWhenNoneAsPhone(self):
            # given
            validator = FormatValidator()

            # when
            validator.check_valid_phone(None)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Phone number is None", "Not recognized none phone number")

        def test_ShouldFailWhenNotValidPhone(self):
            # given
            ko_phone = "_*("
            validator = FormatValidator()

            # when
            validator.check_valid_phone(ko_phone)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Phone number error", "Not recognized phone number error")

    class EmailTests(unittest.TestCase):  # Tests for Email field
        def test_ShouldPassWhenValidEmailFormat(self):
            # given
            email_ok = "foo@bar.com"
            validator = FormatValidator()

            # when
            validator.check_valid_email(email_ok)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldPassWhenEmptyEmail(self):
            # given
            empty_email = ""
            validator = FormatValidator()

            # when
            validator.check_valid_email(empty_email)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldPassWhenNoneAsEmail(self):
            # given
            validator = FormatValidator()

            # when
            validator.check_valid_email(None)

            # then
            self.assertIsNone(validator.error, "Error detected")

        def test_ShouldFailWhenNotValidEmail(self):
            # given
            ko_email = "foo.bar@com"
            validator = FormatValidator()

            # when
            validator.check_valid_email(ko_email)

            # then
            self.assertIsNotNone(validator.error, "No error found, but should!")
            self.assertEqual(validator.error, "Email error", "Not recognized email error")


if __name__ == "__main__":
    unittest.main(FormatValidatorTest)  # Executing our TestSuite
