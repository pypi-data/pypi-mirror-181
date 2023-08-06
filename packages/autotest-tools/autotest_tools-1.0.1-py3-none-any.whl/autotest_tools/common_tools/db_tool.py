from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def elements(db_class, db_path):
    db = db_class()
    engine = create_engine("sqlite:///" + db_path)
    session = sessionmaker(bind=engine)
    db_session = session()
    d = db_session.query(db).all()
    db_session.close()
    return d
