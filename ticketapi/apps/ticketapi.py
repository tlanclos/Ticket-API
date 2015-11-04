import json
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
def update_employee():
    """
    Update Employee page
    :return:
    """
    return 'Ticket-API update-employee URI {data}'.format(data=request.data)


@app.route('/submit-ticket/', methods=['POST'], strict_slashes=False)
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    return 'Ticket-API submit-ticket URI {data}'.format(data=request.data)


