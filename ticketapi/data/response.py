import json
from flask import Response
from ticketapi.data.logger import logger


class FailureResponse(object):
    """
    Failure response contains methods appropriate for creating a standard failure
    response that may be returned when a failure is encountered.

    :param error_code: error code associated with this failure response
    :param nice_message: message that may be displayed to the user if necessary
    :param debug_message: message that should not be displayed to the user, but may be used for bug reports
    """
    error_code = 200
    payload = {}

    def __init__(self, error_code, nice_message, debug_message):
        self.error_code = error_code
        self.payload['niceMessage'] = nice_message
        self.payload['debugMessage'] = debug_message
        logger.error(debug_message)

    def as_json(self):
        """
        Create a JSON string representation of the payload

        :return: JSON string representation of the payload
        """
        return json.dumps(self.payload)

    def response(self):
        """
        Create a flask response object. This object can be returned by a flask routed function in order
        to respond to a request. This is the method that may be used to standardize failure responses from
        this API

        :return: Flask response
        """
        return Response(response=self.as_json(), status=self.error_code, mimetype='application/json')
