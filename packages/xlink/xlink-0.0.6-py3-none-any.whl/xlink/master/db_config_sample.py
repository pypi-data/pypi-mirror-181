import os

# DB
DB_TYPE = 'mysql'
DB_ROOT_PASSWORD = 'root'
DB_NAME = 'test_db'
DB_USER = 'ttt'
DB_PASSWORD = os.getenv('schedule_mysql_password_test', None)
DB_HOST_PORT = 3306
DB_HOST = os.getenv('schedule_mysql_host_test', None)

DB_CONFIG = {
    'DB_ENGINE_CONFIG_PREFIX': 'test.',
    'DB_ENGINE_CONFIG': {
        'test.url': f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_HOST_PORT}/{DB_NAME}?charset=utf8',
        'test.isolation_level': 'REPEATABLE_READ',
        'test.max_overflow': 10,
        'test.pool_size': 5,
        'test.echo': False,
    },
    'DB_ENGINE_POOL_SIZE': 5,
    'DB_ENGINE_MAX_OVERFLOW': 10,
    'DB_SESSION_AUTOFLUSH': True,
    'DB_SESSION_AUTOCOMMIT': False,
}
