import traceback
from ticketapi.data.fields import *
from ticketapi.data.response import *
from werkzeug.exceptions import BadRequest

__all__ = [
    'Validator',
    'EmployeeInfoValidator'
]


class Validator(object):

    fields = []

    def __init__(self, current_request):
        self.current_request = current_request

    def validate(self):
        try:
            try:
                # make Flask decode JSON regardless of content type header
                data = self.current_request.get_json(force=True)
            except BadRequest:
                return FailureResponse(
                    error_code=400,
                    debug_message='Request body is not valid JSON',
                    nice_message='Something went wrong while performing the operation',
                )

            for field in self.fields:
                field_valid = field.validate(data.get(field.name))
                if not field_valid[0]:
                    return FailureResponse(
                        error_code=400,
                        debug_message='Field %s is invalid: %s'.format(field.name, field_valid[1]),
                        nice_message='Field %s is invalid'.format(field.name)
                    )

        except:
            return FailureResponse(
                error_code=520,
                debug_message='An exception occurred during validation, see traceback',
                nice_message='Something went wrong while performing the operation',
                traceback=traceback.format_exc()
            )


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
