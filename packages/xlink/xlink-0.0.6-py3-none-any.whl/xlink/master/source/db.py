from sqlalchemy import engine_from_config
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import event


def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if 'update ' in statement.lower():
        # print('update')
        pass
    if 'delete ' in statement.lower():
        # print('warning delete statement: {}'.format(statement))
        pass
    if 'insert ' in statement.lower():
        pass
    if 'select ' in statement.lower() and 'updated_time' in statement.lower():
        # print(statement)
        pass
    # print('before_cursor_execute')
    # print(statement)


class DbFactory():

    @staticmethod
    def create_engine_from_config(config: dict):
        engine = engine_from_config(config['DB_ENGINE_CONFIG'], prefix=config['DB_ENGINE_CONFIG_PREFIX'])
        if not database_exists(engine.url):
            create_database(engine.url)
        return engine

    @staticmethod
    def create_session_from_config(config: dict):
        engine = DbFactory.create_engine_from_config(config)
        event.listen(engine, 'before_cursor_execute', before_cursor_execute)
        session = sessionmaker()
        session.configure(bind=engine, autoflush=config['DB_SESSION_AUTOFLUSH'], autocommit=config['DB_SESSION_AUTOCOMMIT'])
        s = session()
        return s

    @staticmethod
    def create_engine_and_session_from_config(config: dict):
        engine = DbFactory.create_engine_from_config(config)
        event.listen(engine, 'before_cursor_execute', before_cursor_execute)
        session = sessionmaker()
        session.configure(bind=engine, autoflush=config['DB_SESSION_AUTOFLUSH'], autocommit=config['DB_SESSION_AUTOCOMMIT'])
        s = session()
        return engine, s


class BaseDbManager():

    _engine = None
    _session = None

    def __init__(self, base, config: dict):
        self._base = base
        self._engine, self._session = DbFactory.create_engine_and_session_from_config(config)

    def make_repository(self, db_type, sharding_key):
        raise Exception('BaseDbManager.make_repository should be implement')

    def create_tables(self):
        self._base.metadata.create_all(bind=self._engine)

    def drop_tables(self):
        self._base.metadata.drop_all(bind=self._engine)

    def list_sorted_tables(self):
        return self._base.metadata.sorted_tables

    def get_engine(self):
        return self._engine

    def get_session(self):
        return self._session

    def add(self, model):
        return self._session.add(model)

    def bulk_save_objects(self, models):
        # raise Exception('该方法可能会引起Foraign key的约束造成插入失败')
        return self._session.bulk_save_objects(models)

    def commit(self):
        return self._session.commit()

    def close(self):
        self._session.close()

    def dispose(self):
        self._engine.dispose()
