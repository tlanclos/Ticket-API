from ticketapi.datalayer.wrapper import *
from ticketapi.datalayer.models import Authentication
from ticketapi.datalayer.models import Company
from ticketapi.datalayer.models import Session
from ticketapi.datalayer.models import Ticket
from ticketapi.data.logger import logger
from ticketapi.data.crypto import crypto
from uuid import uuid4
from datetime import datetime
import base64


__all__ = ['add_auth', 'authenticate', 'update_employee', 'submit_ticket', 'check_auth']


def add_auth(**kwargs):
    """
    Add a new company to the database with a provided companyID and password and associate
    this companyID with an existing companyName

    :param kwargs:
        companyName - the company name to associate with this companyID
        companyID - the company identifier to create
        password - password to encrypt and store for this company
    :return: if the companyID already exists or companyName does not exist or
        not all required parameters were passed in, False will be returned and a reason,
        otherwise True and success
    """
    # Get the required values from the kwargs dictionary
    company_name = kwargs.get('companyName')
    company_id = kwargs.get('companyID')
    password = kwargs.get('password')

    # Check if all the values are validly assigned
    if all([company_name, company_id, password]):
        try:
            with DB() as s:
                selected_auth = s.query(Authentication)\
                    .filter(Authentication.companyID == kwargs['companyID'])\
                    .first()

                # Test if there is already a pre-existing companyID with the given value
                if selected_auth is not None:
                    reason = 'companyID already exists'
                    logger.error(reason)
                    return False, reason

                selected_company = s.query(Company)\
                    .filter(Company.CompanyName == company_name)\
                    .first()

                # Test to ensure that there is a company name with the given value
                if selected_company is None:
                    reason = 'companyName "{name}" does not exist'.format(name=company_name)
                    logger.error(reason)
                    return False, reason

                # Generate the hash and salt values
                hashval, saltval = crypto.hash(password)

                # techneaux company identifier
                tech_comp = selected_company.CompanyID

                # Add the new row for the authentication
                new_auth = Authentication(
                    techneauxTechCompanyID=tech_comp,
                    companyID=company_id,
                    hash=base64.standard_b64encode(hashval).decode('ascii'),
                    salt=base64.standard_b64encode(saltval).decode('ascii')
                )
                s.add(new_auth)

                logger.info('Added authentication for {tech_comp} as {comp}'.format(
                    tech_comp=tech_comp,
                    comp=company_id
                ))

                return True, 'Success'
        except Exception as e:
            logger.exception(e)
            return False, str(e)
    else:
        reason = 'companyID, password, and companyName must be provided to add the company'
        logger.error(reason)
        return False, reason


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
            selected_auth = s.query(Authentication)\
                .filter(Authentication.companyID == kwargs['companyID'])\
                .first()

            password_verified = False
            if selected_auth is not None:
                password_verified = crypto.check(
                    kwargs['password'],
                    base64.standard_b64decode(selected_auth.hash),
                    base64.standard_b64decode(selected_auth.salt)
                )

            # If this combination exist, the user provided valid credentials
            if password_verified:
                uuid = str(uuid4())
                company_id = selected_auth.companyID

                # Create a new session row
                new_session = Session(
                    authKey=uuid,
                    creationTime=datetime.now(),
                    companyID=company_id
                )
                s.add(new_session)

                logger.info('Authorized {comp} with new auth {auth}'.format(
                    comp=company_id,
                    auth=uuid
                ))

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

                logger.info('Updated info for {first} {last} as email={email} phone={phone}'.format(
                    first=kwargs.get('firstName'),
                    last=kwargs.get('lastName'),
                    email=kwargs.get('email'),
                    phone=kwargs.get('phoneNumber')
                ))

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
                logger.info('Authorization key {auth} is valid'.format(auth=kwargs['authKey']))
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


if __name__ == '__main__':
    with DB() as session:
        hashed_val, salt_val = crypto.hash('hunter2')
        new_company = Authentication(
            companyID='ayylmao',
            hash=base64.standard_b64encode(hashed_val),
            salt=base64.standard_b64encode(salt_val),
            techneauxTechCompanyID=1400
        )
        session.add(new_company)
