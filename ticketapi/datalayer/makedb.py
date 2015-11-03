from ticketapi.datalayer.models import db
from ticketapi.datalayer.models import Company
from ticketapi.datalayer.wrapper import *

# Create the basic database layout
db.create_all()

# Add a test fake company with a fake password
with DB() as s:
    testCompany = Company(
        companyID='John',
        companyName='Team John',
        password='hunter2'
    )
    s.add(testCompany)
