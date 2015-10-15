from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to Ticket-API!'


@app.route('/login')
def login():
    pass


@app.route('/update-employee')
def update_employee():
    pass


@app.route('/submit-ticket')
def submit_ticket():
    pass


if __name__ == '__main__':
    app.run(port=5000)
