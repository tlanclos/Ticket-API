import json
from flask import make_response


class FailureResponse(object):
    error_code = 200
    payload = {}

    def __init__(self, error_code, nice_message, debug_message, traceback=None):
        self.error_code = error_code
        self.payload['niceMessage'] = nice_message
        self.payload['debugMessage'] = debug_message
        if traceback is not None:
            self.payload['traceback'] = traceback

    def as_json(self):
        return json.dumps(self.payload)

    def response(self):
        return make_response(self.as_json(), self.error_code)


#FailureResponse must take in an error_code, nice_message, debug_message, and a traceback string in its __init__ method.
#
#FailureResponse must implement a method called as_json() which will convert the provided data into json via the json.dumps() method.
#
#FailureResponse must, lastly, implement a method called response() which will return flask's make_response(self.as_json(), self.error_code). If possible, this function may also take in a headers dictionary and update the response headers before returning it.
#
#FailureResponse must also implement logging on a call to response().
