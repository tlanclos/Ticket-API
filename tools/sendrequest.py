"""
This is a rough test script for responses that loads in a json file for
a request. This file will be loaded and a request will be sent to the server
defined in the json file. The request is also specified in the json file.
Given a directory, this script can run all json files within that directory.
The json file should be in the format:

{
  "requests": {
    "login": {
      "uri": "http://localhost:50443/login",
      "payload": {
        "companyID": "TECHNEAUX",
        "password": "techneauxpass"
      },
      "exp_response_code": 200
    },
    "update-employee": {
      "uri": "http://localhost:50443/update-employee",
      "payload": {
        "firstName": "myname",
        "lastName": "mysurname",
        "email": "myname.mysurname@myname.com",
        "phoneNumber": "1235559909",
        "authKey": "{authKey}"
      },
      "exp_response_code": 200
    }
  },
  "tests": {
    "test1": ["login", "update-employee"]
  },
  "test-order": ["test1"]
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
    response = requests.post(url=uri, data=json.dumps(payload), allow_redirects=False, verify=False)
    print('Response Code:', response.status_code)
    print('Response Reason:', response.reason)
    print('==== BODY ====')
    print(response.text)
    print('==== BODY ====')
    print()
    return response.status_code, response.text


def run_file(file):
    """
    Run a test on a single file provided file

    :param file: test file to load
    :return: test fail count
    """
    fail_count = 0
    if file:
        data = load_test(file)

        for test in data.get('test-order'):
            print('running {test}'.format(test=test))
            last_response = SafeFormat()
            for request in data.get('tests').get(test):
                print('running {req}'.format(req=request))
                req = data.get('requests').get(request)
                uri = req['uri']
                exp_code = req.get('exp_response_code', 200)
                payload = {k: v.format(**last_response) if isinstance(v, str) else v for k, v in req['payload'].items()}
                print(uri)
                print(payload)
                try:
                    code, text = send_request(uri=uri, payload=payload)
                    if code != exp_code:
                        print('{test} Failed!'.format(test=test))
                        fail_count += 1
                        break
                    last_response.update(SafeFormat(**json.loads(text)))
                except Exception as e:
                    print(e)
            else:
                print('{test} Passed!'.format(test=test))
            print()
    return fail_count


def run_dir(directory):
    """
    Run all test files within a directory

    :param directory: directory to test
    :return: total fail count of all tests
    """
    total_fail_count = 0
    if directory:
        files = os.listdir(directory)
        tests = [file for file in files if os.path.splitext(file)[1] == '.json']
        for test in tests:
            total_fail_count += run_file(test)
    return total_fail_count


if __name__ == '__main__':
    # Setup the argument parser
    parser = argparse.ArgumentParser(description='Sends a json request to a url')
    parser.add_argument('--file', '-f', help='Load this json file to run')
    parser.add_argument('--dir', '-d', help='Load all json files within this directory and run')

    # Get our arguments
    args = parser.parse_args()

    # Initially we have 0 failed tests
    fail_count = 0

    # Run all files and directories specified
    fail_count += run_file(args.file)
    fail_count += run_dir(args.dir)
    if fail_count > 0:
        print('{count} tests Failed!'.format(count=fail_count))
    else:
        print('All tests Passed!')
