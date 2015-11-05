import json
from flask import request
from flask import jsonify
from ticketapi.apps import app
from ticketapi.data.decorators import *
from ticketapi.data.validators import *
from ticketapi.datalayer.procedures import *
from ticketapi.data.response import FailureResponse
from werkzeug.exceptions import RequestTimeout


@app.route('/')
def home():
    """
    Home page
    :return:
    """
    return 'Welcome to Ticket-API!'


@app.route('/login/', methods=['POST'], strict_slashes=False)
def login():
    """
    Login page
    :return:
    """
    return 'Ticket-API login URI {data}'.format(data=request.data)


@app.route('/update-employee/', methods=['POST'], strict_slashes=False)
def update_employee():
    """
    Update Employee page
    :return:
    """

    json_data = request.get_json(force=True)

    try:
        result = update_employee(**json_data)
        
    except RequestTimeout:
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
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    return 'Ticket-API submit-ticket URI {data}'.format(data=request.data)
