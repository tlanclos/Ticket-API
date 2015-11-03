from ticketapi.datalayer.wrapper import *
from ticketapi.datalayer.models import Company
from ticketapi.datalayer.models import Session
from ticketapi.datalayer.models import Ticket
from ticketapi.data.logger import logger
from uuid import uuid4
from datetime import datetime


__all__ = ['authenticate', 'update_employee', 'submit_ticket', 'check_auth']


def authenticate(**kwargs):
    """
    Authenticate a new session with some given credentials. This will provide the user with a
    new authorization key which will be needed for future reference to the session being created

    :param kwargs:
        companyID - the company identifier created and provided by Techneaux
        password - password to authenticate against, currently this must be the encrypted version of the password
    :return: a new authorization key or False (if bad credentials were provided or the companyID/password was not found)
    """
    if 'companyID' in kwargs and 'password' in kwargs:
        with DB() as s:
            # Query the database for a password and companyID combination
            selected_company = s.query(Company)\
                .filter(Company.companyID == kwargs['companyID'], Company.password == kwargs['password'])\
                .first()

            # If this combination exist, the user provided valid credentials
            if selected_company is not None:

                # Create a new session row
                new_session = Session(
                    authKey=str(uuid4()),
                    creationTime=datetime.now(),
                    companyID=selected_company.companyID,
                    company=selected_company
                )
                s.add(new_session)

                # And return the authorization key
                return new_session.authKey
            else:
                logger.error('Unable to authorize the company {company}, check credentials'.format(
                    company=kwargs.get('companyID')
                ))
                return False
    else:
        logger.error('companyID and password must be provided to the authenticate method')
        return False


def update_employee(**kwargs):
    """
    Update an employee with given information such as name, email and phone. This method must be provided
    with an authorization key, otherwise information will not be added to the database

    :param kwargs:
        authKey - authorization key associated with this employee
        firstName - first name of the employee
        lastName - last name of the employee
        email - email address of the employee
        phoneNumber - phone number of the employee
    :return: True if the employee was updated, False if the employee was not updated
    """
    if 'authKey' in kwargs:
        with DB() as s:
            # Attempt to get an employee associated with the authorization key
            employee = s.query(Session).filter(Session.authKey == kwargs['authKey']).first()

            # If we have a valid employee, then update his/her information
            if employee is not None:
                employee.firstName = kwargs.get('firstName')
                employee.lastName = kwargs.get('lastName')
                employee.email = kwargs.get('email')
                employee.phoneNumber = kwargs.get('phoneNumber')
                return True
            else:
                logger.error('Unable to find an employee associated with the provided authentication key')
                return False
    else:
        logger.error('authKey must be provided for the update_employee method')
        return False


def check_auth(**kwargs):
    """
    Check if an authorization key has been created. If an authorization key has been generated
    then the provided `authKey` was successfully authorized as some point

    :param kwargs:
        authKey - authorization key to test
    :return: True if the the authKey was found in the database, False otherwise
    """
    if 'authKey' in kwargs:
        with DB() as s:
            # Attempt to get an session associated with the auth key
            the_session = s.query(Session.authKey).filter(Session.authKey == kwargs['authKey']).first()

            # If we have a valid session, then they key has been authorized
            if the_session is not None:
                return True
            else:
                logger.error('Unable to find a session associated with the provided authentication key')
    else:
        logger.error('authKey must be provided for the check_auth method')
        return False


def submit_ticket(**kwargs):
    """
    Submit a ticket to the database, this requires that a session has been created and that the ticket has
    at least a description. A location and photo may be provided, but is not required

    :param kwargs:
        authKey - authorization key that has been previously provided by the the API
        description - description of the ticket that is being submitted
        location - physical location (such as a site or address) that the issue is being incurred
        photo - photograph associated with the issue
    :return: True if the ticket has successfully been submitted, False otherwise
    """
    if 'authKey' in kwargs and 'description' in kwargs:
        with DB() as s:
            # Get the session associated with this auth key if one exists
            the_session = s.query(Session).filter(Session.authKey == kwargs['authKey']).first()

            # If we found a session we will create a new ticket
            if the_session is not None:

                # Create the ticket and add it to the database
                new_ticket = Ticket(
                    authKey=kwargs['authKey'],
                    description=kwargs['description'],
                    location=kwargs.get('location'),
                    photo=kwargs.get('photo'),
                    creationTime=datetime.now(),
                    session=the_session
                )
                s.add(new_ticket)

                # We have successfully add a ticket to the database
                return True
            else:
                logger.error('Unable to find a session associated with the provided authentication key')
                return False
    else:
        logger.error('authKey and description must be provided for the submit_ticket method')
        return False
