import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Model = declarative_base()


class SessionFactory(object):
    MYSQL_URI_TEMPLATE = 'mysql://%s:%s@%s/%s'
    Session = None

    def __init__(self, user, password, host, database):
        engine = create_engine(self.MYSQL_URI_TEMPLATE % (user, password, host, database))
        self.Session = sessionmaker(bind=engine)

    def doReadQuery(self, query):
        session = self.Session()
        result = json.dumps(query(session))
        session.close()
        return result

    def doWriteQuery(self, query):
        session = self.Session()
        try:
            result = json.dumps(query(session))
            session.commit()
        except:
            result = None
            session.rollback()
        finally:
            session.close()
        return result
