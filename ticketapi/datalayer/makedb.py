from ticketapi.datalayer.models import db
from ticketapi.datalayer.models import Company
from ticketapi.datalayer.wrapper import *

db.create_all()

with DB() as s:
    testCompany = Company(
        companyID='John',
        companyName='Team John',
        password='hunter2'
    )
    s.add(testCompany)
