import sys
from validate_email import validate_email
import phonenumbers


class Field(object):
    """
    Base field class that validates name and required. When inheriting this class,
    you should implement `_validate(value)` function and also add it to the list of validators
    `self.validators`. For example, StringField's init should call
    `self.validators.append(StringField._validate)` immediately after
    `super().__init__(*args, **kwargs)`.

    :param name: name of the field located within validation data
    :param required: states whether or not the field is required in the validation data
    """
    def __init__(self, name, required=True, **kwargs):
        self.name = name
        self.required = required
        self.default_success_msg = 'Success'
        self.validators = [Field._validate]

    def success(self):
        """
        Helper function to return success message

        :return: tuple (True, default_success_msg)
        """
        return True, self.default_success_msg

    def failure(self, message):
        """
        Helper function to return a failure message

        :param message: message to return
        :return: tuple (False, "data['{name}']: {message}")
        """
        return False, "key={name} :: {msg}".format(name=self.name, msg=message)

    def _validate(self, value):
        """
        Default validation function that always returns success

        :param value: value to validate
        :return: success as a tuple (status, message)
        """
        return self.success()

    def validate(self, data):
        """
        Validation chain function that will look at the list of validate functions
        in self.validators and call them successively until one returns failure or
        all functions have been called

        :param value: data to validate
        :return: success or failure as a tuple (status, message)
        """
        # ensure the value exists if it is required
        value = data.get(self.name)
        if self.required and value is None:
            return self.failure('required but does not exist')

        # if it is not required, but is None, then it is known success
        if value is None:
            return self.success()

        # otherwise, go through our validators and attempt to validate the value
        for validator in self.validators:
            status, message = validator(self, value)
            if not status:
                return status, message
        else:
            return self.success()


class StringField(Field):
    """
    Validates that a field is a string at a particular length

    :param name: name of the field located within validation data
    :param required: states whether or not the field is required in the validation data
    :param min_length: minimum length of the string
    :param max_length: maximum length of the string
    """
    def __init__(self, name, required=True, **kwargs):
        super().__init__(name, required=required, **kwargs)
        self.validators.append(StringField._validate)

        self.min_length = kwargs.get('min_length', 0)
        self.max_length = kwargs.get('max_length', sys.maxsize)

    def _validate(self, value):
        """
        Validates a string by checking if the value is an instance of string class and
        that the length fits within the min and max lengths specified by the field

        :param value: value to validate
        :return: success or failure as a tuple (status, message)
        """
        if not isinstance(value, str):
            return self.failure('not an instance of a string')

        if self.min_length <= len(value) <= self.max_length:
            return self.success()

        return self.failure('not within size bounds {mi} <= len(x) <= {ma}'.format(
            mi=self.min_length,
            ma=self.max_length
        ))


class EmailField(StringField):
    """
    Validates an email field according to RFC 2822

    :param name: name of the field located within validation data
    :param required: states whether or not the field is required in the validation data
    :param min_length: minimum length of the string (should be left as default)
    :param max_length: maximum length of the string (should be left as default)
    """
    def __init__(self, name, required=True, **kwargs):
        super().__init__(name, required=required, **kwargs)
        self.validators.append(EmailField._validate)

    def _validate(self, value):
        """
        Validates an email address according to RFC 2822

        :param value: value to validate
        :return: success or failure as a tuple (status, message)
        """
        if not validate_email(value):
            return self.failure('not a valid email address')

        return self.success()


class PhoneNumberField(StringField):
    """
    Validates phone numbers based on their country code, if a country code
    is not entered, then the country code specified by default_country_code
    is utilized.

    :param name: name of the field located within validation data
    :param required: states whether or not the field is required in the validation data
    :param min_length: minimum length of the string (should be left as default)
    :param max_length: maximum length of the string (should be left as default)
    :param default_country_code: when a number does not have a country code, assume this one
    """
    def __init__(self, name, required=True, **kwargs):
        super().__init__(name, required=required, **kwargs)
        self.validators.append(PhoneNumberField._validate)

        self.default_country_code = kwargs.get('default_country_code', 1)

    def _validate(self, value):
        """
        Validate a phone number based on its country code or the default country code.

        :param value: value to validate
        :return: success or failure as a tuple (status, message)
        """
        # add the country code if one does not already exist
        value = value.strip()
        if not value.startswith('+'):
            value = '+' + str(self.default_country_code) + value

        try:
            # parse the number into a number object (this should hopefully never fail but its possible)
            number = phonenumbers.parse(value)

            # if the phone number is not a valid number based on the country code, then fail
            if not phonenumbers.is_valid_number(number):
                return self.failure('phone number does not match valid pattern for country code {code}'.format(
                    code=number.country_code
                ))
        except Exception as e:
            return self.failure(e)

        return self.success()


if __name__ == '__main__':
    print(StringField('string', required=True).validate({'string': 'bob'}))
    print(StringField('string', min_length=3, max_length=3, required=True).validate({'string': 'bob'}))
    print(StringField('string', min_length=4, max_length=3, required=True).validate({'string': 'bob'}))
    print(StringField('string', min_length=3, max_length=4, required=True).validate({'string': 'bob'}))
    print(StringField('string', required=False).validate({'string2': 'bob'}))
    print(EmailField('email', required=True).validate({'email': 'bob3f@bob'}))
    print(EmailField('email', required=True).validate({'_email': 'bob3f@bob'}))
    print(EmailField('email', required=True).validate({'email': 'bob3f^bob'}))
    print(PhoneNumberField('phone', required=True).validate({'phone': '+442083661178'}))
    print(PhoneNumberField('phone', required=True).validate({'phone': '442083661178'}))
    print(PhoneNumberField('phone', required=True).validate({'phone': '(337)945-5244'}))
    print(PhoneNumberField('phone', required=True).validate({'phone': '3379442213'}))
    print(PhoneNumberField('phone', required=True).validate({'phone': '1234'}))
