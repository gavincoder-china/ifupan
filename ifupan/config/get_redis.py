import redis
from redis.exceptions import AuthenticationError, TimeoutError, RedisError

from ifupan.utils.log_util import logger
from ifupan.config.env import RedisConfig

class RedisUtil:
    """
    Redis相关方法
    """

    @classmethod
    def create_redis_pool_sync(cls):
        """
        应用启动时初始化redis连接

        :return: Redis连接对象
        """
        logger.info('开始连接redis...')
        try:
            redis_client = redis.Redis(
                host=RedisConfig.redis_host,
                port=RedisConfig.redis_port,
                username=RedisConfig.redis_username,
                password=RedisConfig.redis_password,
                db=RedisConfig.redis_database,
                decode_responses=True
            )
            redis_client.ping()
            logger.info('redis连接成功')
            return redis_client
        except AuthenticationError as e:
            logger.error(f'redis用户名或密码错误，详细错误信息：{e}')
            raise
        except TimeoutError as e:
            logger.error(f'redis连接超时，详细错误信息：{e}')
            raise
        except RedisError as e:
            logger.error(f'redis连接错误，详细错误信息：{e}')
            raise

    @staticmethod
    def close_redis_pool_sync(redis_client):
        redis_client.close()

    # @classmethod
    # async def init_sys_config(cls, redis):
    #     """
    #     应用启动时缓存参数配置表
    #
    #     :param redis: redis对象
    #     :return:
    #     """
    #     async with AsyncSessionLocal() as session:
    #         await ConfigService.init_cache_sys_config_services(session, redis)

    # @classmethod
    # async def create_redis_pool(cls) -> aioredis.Redis:
    #     """
    #     应用启动时初始化redis连接

    #     :return: Redis连接对象
    #     """
    #     logger.info('开始连接redis...')
    #     try:
    #         redis = await aioredis.from_url(
    #             url=f'redis://{RedisConfig.redis_host}',
    #             port=RedisConfig.redis_port,
    #             username=RedisConfig.redis_username,
    #             password=RedisConfig.redis_password,
    #             db=RedisConfig.redis_database,
    #             encoding='utf-8',
    #             decode_responses=True,
    #         )
    #         await redis.ping()
    #         logger.info('redis连接成功')
    #         return redis
    #     except AuthenticationError as e:
    #         logger.error(f'redis用户名或密码错误，详细错误信息：{e}')
    #         raise
    #     except TimeoutError as e:
    #         logger.error(f'redis连接超时，详细错误信息：{e}')
    #         raise
    #     except RedisError as e:
    #         logger.error(f'redis连接错误，详细错误信息：{e}')
    #         raise

    # @staticmethod
    # async def close_redis_pool(redis):
    #     await redis.close()
