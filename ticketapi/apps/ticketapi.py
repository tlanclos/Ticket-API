import json
from flask import request
from flask import make_response
from ticketapi.apps import app
from ticketapi.data.response import FailureResponse
from ticketapi.data.logger import logger


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
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        logger.error('unable to parse JSON data, recieved: {data}'.format(data=request.data))
        logger.error(e)

        response = FailureResponse(
            error_code=400,
            nice_message='Bad Request',
            debug_message='The received data was malformed: you must send valid JSON data'
        ).response()
    else:
        logger.info('received valid JSON')

        company_id = data.get('companyID')
        password = data.get('password')

        if all([company_id, password]):
            logger.info('both companyID and password has been received')
            body = json.dumps({'authKey': 'h3r3-is-s0m3-k1nd-0f-4uth-k3y'})
            response = make_response(body, 200)
        else:
            response = FailureResponse(
                error_code=400,
                nice_message='Bad Request',
                debug_message='The received data was malformed: specify both companyID and password'
            ).response()

    return response


@app.route('/update-employee/', methods=['POST'], strict_slashes=False)
def update_employee():
    """
    Update Employee page
    :return:
    """
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        logger.error('unable to parse JSON data, recieved: {data}'.format(data=request.data))
        logger.error(e)

        response = FailureResponse(
            error_code=400,
            nice_message='Bad Request',
            debug_message='The received data was malformed: you must send valid JSON data'
        ).response()
    else:
        logger.info('received valid JSON')

        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        phone_number = data.get('phoneNumber')
        auth_key = data.get('authKey')

        if not auth_key:
            logger.error('did not receive an authorization key')

            response = FailureResponse(
                error_code=401,
                nice_message='Unauthorized',
                debug_message='An authorization key must be passed in with this request'
            ).response()
        elif all([first_name, last_name, email, phone_number]):
            logger.info('firstName, lastName, email, and phoneNumber received')

            if len(auth_key) != 36:
                response = FailureResponse(
                    error_code=401,
                    nice_message='Unauthorized',
                    debug_message='Not a valid authorization key'
                ).response()
            else:
                body = json.dumps({})
                response = make_response(body, 200)
        else:
            response = FailureResponse(
                error_code=400,
                nice_message='Bad Request',
                debug_message='The received data was malformed: specify firstName, lastName, email, and phoneNumber'
            ).response()

    return response


@app.route('/submit-ticket/', methods=['POST'], strict_slashes=False)
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    try:
        data = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        logger.error('unable to parse JSON data, recieved: {data}'.format(data=request.data))
        logger.error(e)

        response = FailureResponse(
            error_code=400,
            nice_message='Bad Request',
            debug_message='The received data was malformed: you must send valid JSON data'
        ).response()
    else:
        logger.info('received valid JSON')

        location = data.get('location')
        description = data.get('description')
        photo = data.get('photo')
        auth_key = data.get('auth_key')

        if not auth_key:
            logger.error('did not receive an authorization key')

            response = FailureResponse(
                error_code=401,
                nice_message='Unauthorized',
                debug_message='An authorization key must be passed in with this request'
            ).response()
        elif all([location, description, photo]):
            logger.info('location, description, and photo received')

            if len(auth_key) != 36:
                response = FailureResponse(
                    error_code=401,
                    nice_message='Unauthorized',
                    debug_message='Not a valid authorization key'
                ).response()
            else:
                body = json.dumps({})
                response = make_response(body, 200)
        else:
            response = FailureResponse(
                error_code=400,
                nice_message='Bad Request',
                debug_message='The received data was malformed: specify location, description, and photo'
            ).response()

    return response
