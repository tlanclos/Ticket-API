from flask import Flask

__all__ = ['app']

app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>/', strict_slashes=False)
def nossl(path):
    return 'We are unable to process your request as this connection is not secured via SSL'


if __name__ == '__main__':
    app.run(port=5080)
