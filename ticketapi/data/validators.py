import json
from ticketapi.data.fields import *
from ticketapi.data.response import *
from werkzeug.exceptions import BadRequest

__all__ = [
    'Validator'
]


class Validator(object):

    fields = []

    def __init__(self, current_request):
        self.current_request = current_request

    def validate(self):
        try:
            self.current_request.get_json(force=True)

            for i in self.fields:
                if False in i.validate(self.current_request.get(i.name)):
                    return FailureResponse()

        except BadRequest:
            return FailureResponse()


class AuthInfoValidator(Validator):
    fields = [
        StringField('companyID', required=True, max_length=64),
        StringField('password', required=True, max_length=16)
    ]


class EmployeeInfoValidator(Validator):
    fields = [
       StringField('first name', required=False, max_length=32),
       StringField('last name', required=False, max_length=32),
       EmailField('email', required=False, max_length=64),
       PhoneNumberField('phone number', required=False, max_length=32),
       StringField('auth key', required=True)
   ]


class TicketInfoValidator(Validator):
    fields = [
        StringField('location', max_length=64),
        StringField('description', required=True, max_length=1024),
        ImageField('photo', required=False),
        StringField('auth key', required=True)
    ]


