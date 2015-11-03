import os
import scrypt
import json

__all__ = ['crypto']


class CryptoConsts:
    PEPPER_FILE = 'test-pepper.json'  # location of JSON pepper file
    HASH_BYTES = 128  # number of bytes for hash
    SALT_BYTES = 128  # number of bytes for salt


class CryptoError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Crypto:
    """
    Provides wrappers for scrypt that help in hashing and checking passwords with salt and pepper
    """

    def __init__(self):
        """
        Loads pepper from filesystem
        """
        self.__load_pepper(CryptoConsts.PEPPER_FILE)

    @staticmethod
    def __get_salt():
        """
        :return: SALT_BYTES number of random bytes suitable for cryptographic use
        """
        return os.urandom(CryptoConsts.SALT_BYTES)

    def __load_pepper(self, file_loc):
        """
        Loads pepper from file at file_loc and sets pepper attribute.
        File should be JSON formatted with a 'pepper' key.
        :param file_loc: file location to load pepper from
        """
        try:
            with open(file_loc, 'r') as pepper_file:
                try:
                    pepper = json.loads(pepper_file.read()).get('pepper')
                except ValueError:
                    raise CryptoError('Error initializing Crypt')
                else:
                    if not pepper:
                        raise CryptoError('Error initializing Crypt')
                    else:
                        self.pepper = bytes(pepper, encoding='utf8')
        except Exception:
            raise CryptoError('Error initializing Crypt')

    def check(self, test_pw, hashed_pw, salt):
        """
        Checks test_pw against hashed_pw by hashing with salt and pepper
        :param test_pw: password to test
        :param hashed_pw: hashed password
        :param salt: salt
        :return: whether test_pw matches hashed_pw when hashed with salt
        """
        try:
            test_hashed = scrypt.hash(test_pw, salt + self.pepper, buflen=CryptoConsts.HASH_BYTES)
            return test_hashed == hashed_pw
        except scrypt.error:
            return False

    def hash(self, password):
        """
        Hashes password with random salt and pepper and returns hashed password and salt
        :param password: password to hash
        :return: tuple of (hashed, salt) containing the hashed password and generated salt
        """
        try:
            salt = self.__get_salt()
        except NotImplementedError:
            raise CryptoError('Could not encrypt password')

        hashed = scrypt.hash(password, salt + self.pepper, buflen=CryptoConsts.HASH_BYTES)

        return hashed, salt


crypto = Crypto()

if __name__ == '__main__':
    hashed, salt = crypto.hash('hereismypassword')
    print(hashed)
    print(salt)
    is_correct = crypto.check('hereismypassword', hashed, salt)
    print(is_correct)
