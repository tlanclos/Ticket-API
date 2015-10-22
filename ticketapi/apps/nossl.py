from ticketapi.apps import app


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>/', strict_slashes=False)
def nossl(path):
    """
    Return a message stating that we are unable to serve the client because they are not secured via SSL

    :param path: path that the client navigated to
    :return: a message stating that we are unable to serve the client because they are not secured via SSL
    """
    return 'We are unable to process your request to {path} as this connection is not secured via SSL'.format(
        path=path
    )
