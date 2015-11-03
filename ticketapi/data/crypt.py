import os
import scrypt
import json

__all__ = ['crypt']


PEPPER_FILE = 'test-pepper.json'

# maximum encrypt and decrypt time in seconds
MAX_SCRYPT_TIME = 7


class CryptError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Crypt:
    def __init__(self, pepper_loc, max_time):
        self.__load_pepper(pepper_loc)
        self.max_scrypt_time = max_time

    def __load_pepper(self, file_loc):
        try:
            with open(file_loc, 'r') as pepper_file:
                try:
                    pepper = json.loads(pepper_file.read()).get('pepper')
                except ValueError:
                    raise CryptError('Error initializing Crypt')
                else:
                    if pepper is None:
                        raise CryptError('Error initializing Crypt')
                    else:
                        self.pepper = bytes(pepper, encoding='utf8')
        except Exception:
            raise CryptError('Error initializing Crypt')

    def check(self, hashed_pw, test_pw):
        try:
            scrypt.decrypt(hashed_pw, test_pw, maxtime=self.max_scrypt_time, encoding=None)
            return True
        except scrypt.error:
            return False

    def encrypt(self, password):
        try:
            salt = self.get_salt()
        except NotImplementedError:
            raise CryptError('Could not encrypt password')

        hashed = scrypt.encrypt(salt + self.pepper, password)

        return hashed, salt

    @staticmethod
    def get_salt():
        return os.urandom(128)


crypt = Crypt(PEPPER_FILE, MAX_SCRYPT_TIME)

if __name__ == '__main__':
    hashed, salt = crypt.encrypt('hereismypasswordhereismypassword')
    is_correct = crypt.check(hashed, 'hereismypasswordhereismypassword')
    print(is_correct)
    is_correct = crypt.check(hashed, 'hereismypasswordhereismypassworD')
    print(is_correct)

