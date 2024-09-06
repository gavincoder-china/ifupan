from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from ifupan.config.env import  GetConfig

config = GetConfig()
db_settings = config.get_database_config()

ASYNC_SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{db_settings.db_username}:{quote_plus(db_settings.db_password)}@'
    f'{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_database}'
)

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=db_settings.db_echo,
    max_overflow=db_settings.db_max_overflow,
    pool_size=db_settings.db_pool_size,
    pool_recycle=db_settings.db_pool_recycle,
    pool_timeout=db_settings.db_pool_timeout,
)
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass
