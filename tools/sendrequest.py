"""
This is a rough test script for responses that loads in a json file for
a request. This file will be loaded and a request will be sent to the server
defined in the json file. The request is also specified in the json file.
Given a directory, this script can run all json files within that directory.
The json file should be in the format:

{
    "uri": "http://localhost:5443/login",
    "payload": {
        ...
    }
}

It is important to note that this will only work with non-ssl connections
currently. As previously mentioned, a better version of this will be
written later.
"""
import os
import json
import requests
import argparse

__author__ = 'taylor'


class SafeFormat(dict):
    """
    Safe format dictionary that converts missing items to empty strings
    for use with str.format(...)
    """
    def __missing__(self, key):
        return ''


def load_test(file):
    """
    Load a json file

    :param file: file to load
    :return: the file loaded in dictionary format
    """
    with open(file, 'r') as j:
        return json.load(j)


def send_request(uri, payload):
    """
    Send a request to the url and print out some response data

    :param url: url the request should be sent to
    :param payload: payload to send with the url
    :return:
    """
    response = requests.post(url=uri, data=json.dumps(payload), allow_redirects=False)
    print('Response Code:', response.status_code)
    print('Response Reason:', response.reason)
    print('==== BODY ====')
    print(response.text)
    print('==== BODY ====')
    print()
    return response.text


def run_file(file):
    """
    Run a test on a single file provided file

    :param file: test file to load
    :return: nothing
    """
    if file:
        data = load_test(file)

        for test in data.get('test-order'):
            last_response = {}
            for request in data.get('tests').get(test):
                req = data.get('requests').get(request)
                uri = req['uri']
                payload = {k: v.format(**last_response) for k, v in req['payload'].items()}
                try:
                    last_response = SafeFormat(**json.loads(send_request(uri=uri, payload=payload)))
                except:
                    last_response = SafeFormat()


def run_dir(directory):
    """
    Run all test files within a directory

    :param directory: directory to test
    :return: nothing
    """
    if directory:
        files = os.listdir(directory)
        tests = [file for file in files if os.path.splitext(file)[1] == '.json']
        for test in tests:
            run_file(test)


if __name__ == '__main__':
    # Setup the argument parser
    parser = argparse.ArgumentParser(description='Sends a json request to a url')
    parser.add_argument('--file', '-f', help='Load this json file to run')
    parser.add_argument('--dir', '-d', help='Load all json files within this directory and run')

    # Get our arguments
    args = parser.parse_args()

    # Run all files and directories specified
    run_file(args.file)
    run_dir(args.dir)
