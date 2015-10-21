from __session_wrapper import *
from __sql_model import db, Company, Session, Ticket
from uuid import uuid4
from datetime import datetime


def authenticate(**kwargs):
    if 'companyID' in kwargs and 'password' in kwargs:
        with DB() as s:
            selected_company = s    .query(Company)\
                                    .filter(    Company.companyID==kwargs['companyID'],
                                                Company.password==kwargs['password'])\
                                    .first()
            if selected_company is not None:
                new_session = Session(
                    authKey=str(uuid4()),
                    creationTime=datetime.now(),
                    companyID=selected_company.companyID,
                    company=selected_company
                )
                s.add(new_session)
                return new_session.authKey
            else:
                return False
    else:
        return False

def update_employee(**kwargs):
    if 'authKey' in kwargs:
        with DB() as s:
            employee = s.query(Session).filter(Session.authKey==kwargs['authKey']).first()
            employee.firstName = kwargs['firstName'] if 'firstName' in kwargs else None
            employee.lastName = kwargs['lastName'] if 'lastName' in kwargs else None
            employee.email = kwargs['email'] if 'email' in kwargs else None
            employee.phoneNumber = kwargs['phoneNumber'] if 'phoneNumber' in kwargs else None
            return True
    else:
        return False

def submit_ticket(**kwargs):
    if 'authKey' in kwargs and 'description' in kwargs :
        with DB() as s:
            the_session = s.query(Session).filter(Session.authKey==kwargs['authKey']).first()
            if the_session is not None:
                new_ticket = Ticket(
                    authKey=kwargs['authKey'],
                    description=kwargs['description'],
                    location=kwargs['location'] if 'location' in kwargs else None,
                    photo=kwargs['photo'] if 'photo' in kwargs else None,
                    creationTime=datetime.now(),
                    session=the_session
                )
                s.add(new_ticket)
                return True
            else:
                return False
    else:
        return False
