import time
import threading
import traceback
from datetime import datetime
from datetime import timezone
from loguru import logger


class ScheduleDictMaker:

    @staticmethod
    def make_from_orms_by_id(orms):
        assert type(orms) == list
        return {orm.id: ScheduleDictMaker.make_from_orm(orm) for orm in orms}

    @staticmethod
    def make_from_orm(orm):
        # print(orm.id)
        _dict = {}
        _dict['id'] = orm.id
        _dict['key'] = orm.key
        _dict['name'] = orm.name
        _dict['sharding_key'] = orm.sharding_key
        _dict['region'] = orm.region
        _dict['stop_time'] = orm.stop_time
        _dict['version'] = orm.version
        _dict['created_time'] = orm.created_time.isoformat()
        _dict['updated_time'] = orm.updated_time.isoformat()
        return _dict


class ScheduleLoader(threading.Thread):

    # global_last_offset是当前的增量加载时间戳

    def __init__(self, repository_read, schedule_queue, load_limit_num=11111):
        threading.Thread.__init__(self)
        self._last_offset = datetime.fromtimestamp(0, timezone.utc)
        self._repository_read = repository_read
        self._schedule_queue = schedule_queue
        self._load_limit_num = load_limit_num
        self._sort_field_name = 'updated_time'
        self._is_active = True
        self.daemon = True

    def log_timer(self, interval):
        try:
            logger.debug(f'ScheduleLoader log, current schedule_queue size: {self._schedule_queue.qsize()}')
        except Exception:
            logger.error(traceback.print_exc())
        finally:
            t = threading.Timer(interval, self.log_timer, args=(interval, ))
            t.daemon = True
            t.start()

    def load_need_run_once(self):
        try:
            need_run_schedule_orms, self._last_offset = self._repository_read.load_schedules_incr(
                self._sort_field_name,
                last_offset=self._last_offset,
                limit=self._load_limit_num,
            )
            for _schedule_orm in need_run_schedule_orms:
                schedule = ScheduleDictMaker.make_from_orm(_schedule_orm)
                schedule_key = schedule['key']
                self._schedule_queue.put(schedule_key)
                logger.debug(f'load_need_run_once put schedule, schedule={schedule}')
            return len(need_run_schedule_orms)
        except Exception as e:
            logger.error(f'load_need_run_once exception {e}, {traceback.print_exc()}')

    def run(self):
        self.log_timer(10)
        while self._is_active:
            try:
                need_run_num = self.load_need_run_once()
                logger.debug(f'need_run_num = {need_run_num}')
            except Exception as e:
                logger.error(f'{e}, {traceback.print_exc()}')
            finally:
                if need_run_num < self._load_limit_num:
                    time.sleep(2)
