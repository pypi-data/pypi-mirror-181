from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, text, Index, UniqueConstraint, DateTime, BigInteger
from sqlalchemy import event
# from sqlalchemy import TIMESTAMP, JSON

Base = declarative_base()
metadata = Base.metadata


class ScheduleOrm(Base):
    '''
    schedule和schedule strategy从职责的角度最好分开表，但是从触发更新时间和扫描模式更适合合并，所以先合并一个表，读到内存后再以对象存在
    '''
    __tablename__ = 'schedule'
    __table_args__ = (
        UniqueConstraint('key', name='uniq_key'),
        Index('idx_updated_time', 'updated_time'),
        {
            'mysql_collate': 'utf8_general_ci',
            'mysql_engine': 'InnoDB',
            'mysql_default_charset': 'utf8',
        },
    )

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    key = Column(String(100, collation='utf8_general_ci'), unique=True, nullable=False)
    name = Column(String(255, collation='utf8_general_ci'), nullable=False)
    sharding_key = Column(String(10, collation='utf8_general_ci'), nullable=False)
    region = Column(String(10, collation='utf8_general_ci'), nullable=False)
    stop_time = Column(BigInteger, nullable=False)
    version = Column(Integer, nullable=False)
    created_time = Column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_time = Column(DateTime(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


@event.listens_for(ScheduleOrm, 'before_insert')
def do_before_insert(mapper, connect, target):
    print('do_before_insert')
    print(target.sharding_key)


@event.listens_for(ScheduleOrm, 'before_update')
def do_before_update(mapper, connection, target):
    print('do_before_update')
    print(target.sharding_key)


@event.listens_for(ScheduleOrm, 'load')
def receive_load(target, context):
    print('receive_load')
    print(target.sharding_key)


@event.listens_for(ScheduleOrm.sharding_key, 'modified')
def receive_modified(target, initiator):
    print('receive_bulk_replace')
    print(target.sharding_key)
    print(initiator)
