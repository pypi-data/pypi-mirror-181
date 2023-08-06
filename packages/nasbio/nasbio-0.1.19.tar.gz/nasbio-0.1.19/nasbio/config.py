import os
import pathlib
from typing import Optional
from functools import lru_cache
from multiprocessing import cpu_count


class BaseConfig:
    SERVER_ID: str = pathlib.Path(os.getcwd()).parts[-1]
    PROCESS_COUNT: int = cpu_count()

    # Message broker configs.
    MESSAGE_BROKER_URL = \
        f'amqp://{os.environ.get("MESSAGE_BROKER_USER", "guest")}' \
        f':{os.environ.get("MESSAGE_BROKER_PASSWORD", "guest")}' \
        f'@{os.environ.get("MESSAGE_BROKER_HOST")}:{os.environ.get("MESSAGE_BROKER_PORT", 5672)}/%2f'

    # SQLAlchemy configs.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PG_USER = os.environ.get('PG_USER', 'postgres')
    PG_PASSWORD: Optional[str] = os.environ.get('PG_PASSWORD')
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_PORT', 5432)
    PG_DB = os.environ.get('PG_DB', SERVER_ID if os.environ.get('FASTAPI_ENV') == 'production' else f'{SERVER_ID}_dev')

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql+psycopg2://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self):
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}'

    # Celery configs.
    # broker_url = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT", 6379)}/0'
    broker_url = f'amqp://{os.environ.get("RABBITMQ_DEFAULT_USER")}:{os.environ.get("RABBITMQ_DEFAULT_PASS")}' \
                 f'@{os.environ.get("RABBITMQ_HOST")}:{os.environ.get("RABBITMQ_PORT")}'
    result_backend = f'redis://{os.environ.get("REDIS_HOST")}:{os.environ.get("REDIS_PORT", 6379)}/0'
    accept_content = ['application/json']
    task_serializer = 'json'
    result_serializer = 'json'
    redis_max_connections = 5


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True


class DevInMemoryConfig(BaseConfig):
    """Development configuration with sqlite in memory."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///file:rnas?mode=memory&cache=shared&uri=true'
    ASYNC_SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:///file:rnas?mode=memory&cache=shared&uri=true'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False


class ProdInMemoryConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///file:rnas?mode=memory&cache=shared&uri=true'
    ASYNC_SQLALCHEMY_DATABASE_URI = 'sqlite+aiosqlite:///file:rnas?mode=memory&cache=shared&uri=true'


class TestingConfig(BaseConfig):
    """Default testing configuration with sqlite in memory."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestingConfigPG(BaseConfig):
    """Testing configuration with PostgreSQL."""
    TESTING = True


@lru_cache()
def get_settings():
    config_cls_dict = {
        'development': DevelopmentConfig,
        'dev_inmemory': DevInMemoryConfig,
        'production': ProductionConfig,
        'prod_inmemory': ProdInMemoryConfig,
        # Use PostgreSQL DB if USE_PG environment variable is set, else default to inmemory sqlite for testing.
        'testing': TestingConfigPG if os.environ.get('USE_PG', '') else TestingConfig,
    }

    config_name = os.environ.get('FASTAPI_ENV', 'development')
    config_cls = config_cls_dict[config_name]

    return config_cls()


settings = get_settings()
