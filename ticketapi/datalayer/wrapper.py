from ticketapi.datalayer.models import db
from ticketapi.data.logger import logger


__all__ = ['DB']


class DB(object):
    """
    This class is used to create a new database session object that
    can be used with python's `with` statements
    """

    def __enter__(self):
        """
        Get a session object that can be queried

        :return: the database's session object
        """
        return db.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Handle any exception that may have been thrown by the session query

        :param exc_type: exception type that was thrown
        :param exc_val: exception's value
        :param exc_tb: exception's traceback
        :return: the return value will determine if the exception that was caught will be re-raised
        after the call to __exit__ is over. If False, the exception will be re-raised, otherwise it will not
        """
        if exc_type is not None:
            # If we got an exception, we will rollback any changes. This is used as enforcement
            # for, if used correctly, will guarantee that bad data does not get inserted into the database
            logger.error('An exception was caught while querying the database, rolling back any changes')
            db.session.rollback()
            return False
        else:
            # If we successfully ran through the with statement, we will commit any changes that were made
            db.session.commit()
            return True
