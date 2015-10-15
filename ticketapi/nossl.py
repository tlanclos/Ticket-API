from flask import Flask

__author__ = 'Taylor'

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def nossl(path):
    return 'We are unable to process your request as this connection is not secured via SSL'


if __name__ == '__main__':
    app.run(port=5080)
