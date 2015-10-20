import sys
from validate_email import validate_email


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

        :param data: data to validate
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