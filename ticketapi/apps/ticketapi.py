from flask import request
from flask import jsonify
from ticketapi.apps import app
from ticketapi.data.decorators import *
from ticketapi.data.validators import *
from ticketapi.datalayer.procedures import *
from ticketapi.data.response import FailureResponse


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page
    :return:
    """
    return 'Welcome to Ticket-API!'


@app.route('/login/', methods=['POST'], strict_slashes=False)
@requires_validation(AuthInfoValidator)
def login():
    """
    Login page
    :return:
    """
    json_data = request.get_json(force=True)

    try:
        result = authenticate(**json_data)
    except:
        return FailureResponse(
            error_code=408,
            nice_message='There was an error authenticating you with the server',
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
def update_employee():
    """
    Update Employee page
    :return:
    """

    json_data = request.get_json(force=True)

    try:
        result = update_employee(**json_data)
        
    except:
        return FailureResponse(
            nice_message='ERROR 408 Request Timeout',
            debug_message='The database server is not responding or is down.',
            error_code=408
        ).response()

    if result is False:
        return FailureResponse(
            nice_message='ERROR 401 Unauthorized',
            debug_message='Session ID not found.',
            error_code=401
        ).response()

    else:
        return jsonify({})


@app.route('/submit-ticket/', methods=['POST'], strict_slashes=False)
@requires_auth
@requires_validation(TicketInfoValidator)
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """

    ticket_data = request.get_json()

    try:
        result = submit_ticket(**ticket_data)
    except:
        return FailureResponse(
            error_code=408,
            nice_message='There was trouble submitting your ticket to the database',
            debug_message='Unable to reach the database. Request Timeout.'
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
