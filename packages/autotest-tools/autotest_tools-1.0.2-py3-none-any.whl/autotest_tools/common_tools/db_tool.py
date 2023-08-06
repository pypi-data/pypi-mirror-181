from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_tab_fields(db_class, db_path):
    """
    获取表的所有字段
    :param db_class: 表类，如：class ElementDB(base)
    :param db_path: 数据库路径
    :return: 表的所有字段
    """
    db = db_class()
    engine = create_engine("sqlite:///" + db_path)
    session = sessionmaker(bind=engine)
    db_session = session()
    d = db_session.query(db).all()
    db_session.close()
    return d
