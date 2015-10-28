import json
from ticketapi.data.fields import *
from ticketapi.data.response import *
from werkzeug.exceptions import BadRequest

__all__ = [
    'Validator'
]


class Validator(object):
    """
    Base validator class that validates the 'current_request' given. When inheriting this class
    each concrete validator should override the 'fields' attribute with a list of
    concrete data to be validated.

    :param current_request: request that needs to be validated
    """

    fields = []

    def __init__(self, current_request):
        self.current_request = current_request

    def validate(self):
        """
        Validate function that checks to make sure 'current_request' is in correct
        JSON syntax. If syntax is correct JSON, 'current_request' is checked to make sure that
        each required field is present.

        :return: FailureResponse object containing data associated with it's failure.
        """
        try:
            self.current_request.get_json(force=True)

            for i in self.fields:
                if False in i.validate(self.current_request.get(i.name)):
                    return FailureResponse(error_code=400, nice_message='ERROR 400 Bad Request',
                                           debug_message='Field was required, but does not exist.').response()

        except BadRequest:
            return FailureResponse(error_code=400, nice_message='ERROR 400 Bad Request',
                                   debug_message='Request was malformed. JSON syntax was invalid. '
                                                 'Please reformat and try again.').response()


class AuthInfoValidator(Validator):
    """
    Overrides the 'fields' attribute with the concrete data to be validated.
    In this case, 'fields' is re-defined to have two 'StringField's.
    """
    fields = [
        StringField('companyID', required=True, max_length=64),
        StringField('password', required=True, max_length=16)
    ]


class EmployeeInfoValidator(Validator):
    """
    Overrides the 'fields' attribute with the concrete data to be validated.
    In this case, 'fields' is re-defined to have three 'StringField(s)', an
    'EmailField', and a 'PhoneNumberField'.
    """
    fields = [
       StringField('firstName', required=False, max_length=32),
       StringField('lastName', required=False, max_length=32),
       EmailField('email', required=False, max_length=64),
       PhoneNumberField('phoneNumber', required=False, max_length=32),
       StringField('authKey', required=True)
   ]


class TicketInfoValidator(Validator):
    """
    Overrides the 'fields' attribute with the concrete data to be validated.
    In this case, 'fields' is re-defined to have three 'StringField(s)' and
    and 'ImageField'.
    """
    fields = [
        StringField('location', max_length=64),
        StringField('description', required=True, max_length=1024),
        ImageField('photo', required=False),
        StringField('authKey', required=True)
    ]


