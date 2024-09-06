from contextlib import asynccontextmanager
from config.database import AsyncSessionLocal, Base, async_engine
from utils.log_util import logger

@asynccontextmanager
async def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接

    :return:
    """
    async with AsyncSessionLocal() as current_db:
        try:
            yield current_db
        finally:
            await current_db.close()


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
