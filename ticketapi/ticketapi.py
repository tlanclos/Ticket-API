from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/')
def home():
    """
    Home page
    :return:
    """
    return 'Welcome to Ticket-API!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page
    :return:
    """
    return 'Ticket-API login URI {data}'.format(data=request.data)


@app.route('/update-employee', methods=['POST'])
def update_employee():
    """
    Update Employee page
    :return:
    """
    return 'Ticket-API update-employee URI {data}'.format(data=request.data)


@app.route('/submit-ticket', methods=['POST'])
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    return 'Ticket-API submit-ticket URI {data}'.format(data=request.data)


if __name__ == '__main__':
    app.run(port=5443)
