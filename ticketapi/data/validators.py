import json
from ticketapi.data.fields import *
from ticketapi.data.response import *

__all__ = [
    'Validator'
]


class Validator(object):

    fields = []

    def __init__(self, current_request):
        self.current_request = current_request

    def validate(self, string_data):
        try:
            data = json.loads(string_data)

            for i in self.fields:
                if False in i.validate(data.get(i.name)):
                    return FailureResponse()

        except:
            return FailureResponse()


class AuthInfoValidator(Validator):

    def __init__(self, company_id, password):
        self.fields.append(StringField(company_id, True, max_length=64))
        self.fields.append(StringField(password, True, max_length=16))


class EmployeeInfoValidator(Validator):
    def __init__(self, first_name, last_name, email, phone_number, auth_key):
        self.fields.append(StringField(first_name, False, max_length=32))
        self.fields.append(StringField(last_name, False, max_length=32))
        self.fields.append(EmailField(email, False, max_length=64))
        self.fields.append(PhoneNumberField(phone_number, False, max_length=32))
        self.fields.append(StringField(auth_key, True))


class TicketInfoValidator(Validator):
    def __init__(self, location, description, photo, auth_key):
        self.fields.append(StringField(location, max_length=64))
        self.fields.append(StringField(description, True, max_length=1024))
        self.fields.append(ImageField(photo, False))
        self.fields.append(StringField(auth_key, True))


