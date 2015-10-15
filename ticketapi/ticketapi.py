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
    pass


@app.route('/update-employee')
def update_employee():
    """
    Update Employee page
    :return:
    """
    pass


@app.route('/submit-ticket')
def submit_ticket():
    """
    Submit Ticket page
    :return:
    """
    pass


if __name__ == '__main__':
    app.run(port=5000)
