import traceback
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from .db import BaseDbManager
from .schedule_orm import Base
from .schedule_orm import ScheduleOrm
from ...common.tools import validate_utc_iso8601
from loguru import logger


class ScheduleDbManager(BaseDbManager):

    def __init__(self, db_config: dict):
        super().__init__(Base, db_config)

    def make_repository(self, db_type, sharding_key):
        if db_type == 'mysql':
            return ScheduleRepository(self._session, sharding_key)
        raise Exception('unknown db_type: {db_type}')


class ScheduleRepositoryFactory:

    @staticmethod
    def make(db_config, db_type, sharding_key):
        return ScheduleDbManager(db_config).make_repository(db_type, sharding_key)


class ScheduleRepository:

    # _offset可以是更新时间的datetime，也可以是id

    _pool: None
    _sharding_key: str = None

    def __init__(self, pool, sharding_key):
        self._pool = pool
        self._sharding_key = sharding_key

    _schedule_base_entities = (
        ScheduleOrm.id,
        ScheduleOrm.key,
        ScheduleOrm.name,
        ScheduleOrm.sharding_key,
        ScheduleOrm.region,
        ScheduleOrm.stop_time,
        ScheduleOrm.version,
        ScheduleOrm.created_time,
        ScheduleOrm.updated_time,
    )

    def get_schedule_by_key(self, key):
        try:
            schedule = self._pool.query(ScheduleOrm)\
                .with_entities(*self._schedule_base_entities)\
                .filter(ScheduleOrm.schedule_key == key)\
                .first()
            self._pool.commit()
            return schedule
        except Exception as e:
            self._pool.rollback()
            logger.error(e)
        finally:
            pass

    def load_schedules_by_key_list(self, key_list):
        try:
            schedules = self._pool.query(ScheduleOrm)\
                .with_entities(*self._schedule_base_entities)\
                .filter(ScheduleOrm.schedule_key.in_(key_list))\
                .all()
            self._pool.commit()
            return schedules
        except Exception as e:
            self._pool.rollback()
            logger.error(e)
        finally:
            pass

    def load_schedules_incr(self, sort_field_name, last_offset, limit=11111):
        # 增量拉数据
        sort_field = getattr(ScheduleOrm, sort_field_name)
        all_schedules = []
        next_offset = last_offset
        try:
            corner_schedules = self._pool.query(ScheduleOrm)\
                .with_entities(*self._schedule_base_entities)\
                .filter(sort_field == last_offset)\
                .all()
            corner_schedules_len = len(corner_schedules)
            if corner_schedules_len >= limit:
                all_schedules = corner_schedules
                next_offset = next_offset + timedelta(seconds=1)
            else:
                # 如果schedule state num < limit，则拉取大于last_offset的schedule state，limit （schedule state num - limit）个，返回new schedule states
                upper_schedules = self._pool.query(ScheduleOrm)\
                    .with_entities(*self._schedule_base_entities)\
                    .filter(sort_field > last_offset)\
                    .order_by(sort_field.asc())\
                    .limit(limit - corner_schedules_len)\
                    .all()
                if len(upper_schedules) > 0:
                    next_offset = getattr(upper_schedules[-1], sort_field_name)
                else:
                    if corner_schedules_len > 0:
                        next_offset = next_offset + timedelta(seconds=1)
                all_schedules = corner_schedules + upper_schedules
        except Exception as e:
            self._pool.rollback()
            logger.error(f'{e}, {traceback.print_exc()}')
        finally:
            return all_schedules, next_offset

    # def load_limit_need_init_schedules(self, sort_field_name, limit=222):
    #     sort_field = getattr(ScheduleOrm, sort_field_name)
    #     try:
    #         need_init_schedules = self._pool.query(ScheduleOrm)\
    #             .with_entities(*self._schedule_base_entities)\
    #             .filter(sort_field == '')\
    #             .limit(limit)\
    #             .all()
    #     except Exception as e:
    #         self._pool.rollback()
    #         logger.error(f'{e}, {traceback.print_exc()}')
    #     finally:
    #         return need_init_schedules

    # def load_limit_need_run_schedules(self, sort_field_name, current_offset, last_offset, limit=11111):
    #     """
    #     这里的limit只能限制大概的范围，不能保证实际返回的量一定小于等于limit，因为有边缘情况需要加上，所以实际返回量有可能大于limit
    #     当last_offset为''时，转换为'2017-04-10T02:00:00+00:00'
    #     """
    #     if last_offset == '':
    #         last_offset = '2017-04-10T02:00:00+00:00'
    #     assert validate_utc_iso8601(last_offset), last_offset
    #     assert validate_utc_iso8601(current_offset), current_offset
    #     sort_field = getattr(ScheduleOrm, sort_field_name)
    #     all_schedules = []
    #     next_offset = last_offset
    #     try:
    #         # 先拉取等于last_offset的schedule states，并记录数量schedule state num
    #         corner_schedules = self._pool.query(ScheduleOrm)\
    #             .with_entities(*self._schedule_base_entities)\
    #             .filter(sort_field == last_offset)\
    #             .all()
    #         corner_schedules_len = len(corner_schedules)
    #         if corner_schedules_len >= limit:
    #             all_schedules = corner_schedules
    #             next_offset = (datetime.fromisoformat(last_offset) + timedelta(seconds=1)).astimezone(timezone.utc).isoformat()
    #         else:
    #             # 如果schedule state num < limit，则拉取大于last_offset的schedule state，limit （schedule state num - limit）个，返回new schedule states
    #             upper_schedules = self._pool.query(ScheduleOrm)\
    #                 .with_entities(*self._schedule_base_entities)\
    #                 .filter(sort_field > last_offset)\
    #                 .filter(sort_field <= current_offset)\
    #                 .order_by(sort_field.asc())\
    #                 .limit(limit - corner_schedules_len)\
    #                 .all()
    #             if len(upper_schedules) == 0:
    #                 all_schedules = corner_schedules
    #                 next_offset = current_offset
    #             else:
    #                 new_offset = getattr(upper_schedules[-1], sort_field_name)
    #                 all_schedules = corner_schedules + upper_schedules
    #                 next_offset = datetime.fromisoformat(new_offset).astimezone(timezone.utc).isoformat()
    #         self._pool.commit()
    #     except Exception as e:
    #         self._pool.rollback()
    #         logger.error(f'{e}, {traceback.print_exc()}')
    #     finally:
    #         return all_schedules, next_offset

    def close(self):
        self._pool.close()
