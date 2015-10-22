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

class EmployeeInfoValidator(Validator):
    pass
