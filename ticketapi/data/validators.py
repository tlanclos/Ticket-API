from ticketapi.data.fields import *
from ticketapi.data.response import *
from werkzeug.exceptions import BadRequest

__all__ = [
    'Validator',
    'EmployeeInfoValidator',
    'AuthInfoValidator',
    'TicketInfoValidator'
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
                success, reason = field.validate(data.get(field.name))
                if not success:
                    return FailureResponse(
                        error_code=400,
                        debug_message='Field {name} is invalid: {reason}'.format(
                            name=field.name,
                            reason=reason
                        ),
                        nice_message='Field {name} is invalid'.format(name=field.name)
                    )
        except:
            return FailureResponse(
                error_code=520,
                debug_message='An exception occurred during validation, see traceback',
                nice_message='Something went wrong while performing the operation',
            )


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
