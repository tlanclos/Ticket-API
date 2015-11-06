from flask import request
from functools import wraps
from ticketapi.data.response import FailureResponse
from ticketapi.datalayer.procedures import check_auth
from werkzeug.exceptions import BadRequest

__all__ = ['requires_validation', 'requires_auth']


def requires_validation(validator):
    """
    Decorates a view to allow for request validation.  If validation fails,
    the view will not be called--instead the failure response returned by
    the validator will be returned as a flask response.
    If validation is successful, the view will be called unaffected.
    :param validator: a concrete Validator
    :return: the requires validation decorator
    """
    def decorator(view):
        @wraps(view)
        def view_wrapper(*args, **kwargs):
            v = validator(request)
            response = v.validate()

            # if the validator didn't return anything,
            # the request was validated
            if response is None:
                return view(*args, **kwargs)
            else:
                return response.response()
        return view_wrapper
    return decorator


def requires_auth(view):
    """
    Decorates a view to allow for authentication checking.  If authentication fails,
    the view will not be called--instead a failure response will be returned as
    a flask response.
    If authentication is successful, the view will be called unaffected.
    :return: the requires authentication decorator
    """
    @wraps(view)
    def view_wrapper(*args, **kwargs):
        nice_msg = 'There was an error authenticating you with the server'

        # parse JSON
        try:
            json_data = request.get_json(force=True)
        except BadRequest:
            return FailureResponse(
                error_code=400,
                debug_message='Request body could not be parsed as JSON',
                nice_message=nice_msg
            ).response()

        # test whether auth key is in JSON
        auth_key = json_data.get('authKey')
        if auth_key is None:
            return FailureResponse(
                error_code=401,
                debug_message='JSON was missing authentication key',
                nice_message=nice_msg
            ).response()

        try:
            # check authentication
            if check_auth(authKey=auth_key):
                return view(*args, **kwargs)
            else:
                return FailureResponse(
                    error_code=401,
                    debug_message='Authentication key is invalid',
                    nice_message=nice_msg
                ).response()
        except:
            return FailureResponse(
                error_code=520,
                debug_message='Exception occurred when querying database.  Maybe the db is down',
                nice_message=nice_msg
            ).response()

    return view_wrapper
