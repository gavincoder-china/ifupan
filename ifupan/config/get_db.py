from contextlib import contextmanager
from config.database import SessionLocal, Base, engine
from utils.log_util import logger

@contextmanager
def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接

    :return:
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_create_table():
    """
    应用启动时初始化数据库连接

    :return:
    """
    try:
        logger.info('初始化数据库连接...')
        Base.metadata.create_all(bind=engine)
        logger.info('数据库连接成功')
    except Exception as e:
        logger.error(f'数据库连接失败: {str(e)}')
        raise
