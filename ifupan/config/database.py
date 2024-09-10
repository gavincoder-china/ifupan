from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus
from ifupan.config.env import GetConfig

config = GetConfig()
db_settings = config.get_database_config()

SQLALCHEMY_DATABASE_URL = (
    f'mysql+pymysql://{db_settings.db_username}:{quote_plus(db_settings.db_password)}@'
    f'{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_database}'
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=db_settings.db_echo,
    max_overflow=db_settings.db_max_overflow,
    pool_size=db_settings.db_pool_size,
    pool_recycle=db_settings.db_pool_recycle,
    pool_timeout=db_settings.db_pool_timeout,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
