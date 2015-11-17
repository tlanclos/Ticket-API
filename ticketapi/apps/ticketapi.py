from flask import request
from flask import jsonify
from ticketapi.apps import app
from ticketapi.data.decorators import *
from ticketapi.data.validators import *
from ticketapi.datalayer.procedures import *
from ticketapi.data.response import FailureResponse
from ticketapi.data.logger import logger


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page

    :return: home page that says Welcome to Ticket-API
    """
    return 'Welcome to Ticket-API!'


@app.route('/login/', methods=['POST'], strict_slashes=False)
@requires_validation(AuthInfoValidator)
def login_route():
    """
    Login page will authorize a customer given a set of credentials. If there is success, an authKey will
    be provided in json format in the body of the response, otherwise a failure response with a standard
    layout will be sent back in the body.

    :return: a response object with the appropriate body and response code
    """
    json_data = request.get_json(force=True)

    try:
        result = authenticate(**json_data)
    except Exception as e:
        logger.exception(e)
        return FailureResponse(
            error_code=520,
            nice_message='An error occurred while authenticating you',
            debug_message='An exception occurred while trying to query the database'
        ).response()

    if result is False:
        return FailureResponse(
            error_code=401,
            nice_message='The company ID or password was incorrect, please try again',
            debug_message='Invalid company ID or password'
        ).response()

    return jsonify(authKey=result)


@app.route('/update-employee/', methods=['POST'], strict_slashes=False)
@requires_auth
@requires_validation(EmployeeInfoValidator)
def update_employee_route():
    """
    Update Employee will update employee information in the database with an associated session id (authKey). This
    key must provided in the request, otherwise this function will not run (will be stopped by the decorator
    requires_auth). If that an the information was validated, then this function will update the employee's info.

    :return: an empty json body response on success and standard failure response json on failure.
    """

    json_data = request.get_json(force=True)

    try:
        result = update_employee(**json_data)
    except Exception as e:
        logger.exception(e)
        return FailureResponse(
            error_code=520,
            nice_message='An error occurred while updating your information',
            debug_message='The database server is not responding or is down.'
        ).response()

    if result is False:
        return FailureResponse(
            error_code=401,
            nice_message='There was an error authenticating your request',
            debug_message='Session ID not found.'
        ).response()

    else:
        return jsonify({})


@app.route('/submit-ticket/', methods=['POST'], strict_slashes=False)
@requires_auth
@requires_validation(TicketInfoValidator)
def submit_ticket_route():
    """
    Submit Ticket will submit a ticket to the database. This function requires authentication before being ran and
    must be passed an authKey in the json body in order to run. If all information is validated, this function will
    submit the ticket to the database using submit_ticket.

    :return: an empty json body response on success and standard failure response json on failure.
    """

    ticket_data = request.get_json(force=True)

    try:
        result = submit_ticket(**ticket_data)
    except Exception as e:
        logger.exception(e)
        return FailureResponse(
            error_code=520,
            nice_message='There was trouble submitting your ticket to the database',
            debug_message='Unable to reach the database.'
        ).response()

    if result is False:
        return FailureResponse(
            error_code=400,
            nice_message='There was trouble submitting your ticket to the database. The data may be invalid.',
            debug_message='Malformed/Invalid data request sent to database'
        ).response()

    return jsonify({})


if __name__ == '__main__':
    app.debug = True
    app.run(port=50443)
