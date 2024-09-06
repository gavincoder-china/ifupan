from config.database import async_engine, AsyncSessionLocal, Base
from utils.log_util import logger


def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接

    :return:
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_create_table():
    """
    应用启动时初始化数据库连接

    :return:
    """
    try:
        logger.info('初始化数据库连接...')
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info('数据库连接成功')
    except Exception as e:
        logger.error(f'数据库连接失败: {str(e)}')
        raise
