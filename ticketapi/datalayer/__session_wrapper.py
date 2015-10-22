from __sql_model import db, Company, Session, Ticket

class DB(object):
    def __enter__(self):
        return db.session
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            db.session.rollback()
            return False
        else:
            db.session.commit()
            return True
