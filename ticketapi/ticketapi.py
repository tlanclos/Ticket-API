from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    """
    Home page
    :return:
    """
    return 'Welcome to Ticket-API!'


@app.route('/login')
def login():
    """
    Login page
    :return:
    """
    return 'Ticket-API login URI'


@app.route('/update-employee')
def update_employee():
    """
    Update Employee page
    :return:
    """
    return 'Ticket-API update-employee URI'


@app.route('/submit-ticket')
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    return 'Ticket-API submit-ticket URI'


if __name__ == '__main__':
    app.run(port=5443)
