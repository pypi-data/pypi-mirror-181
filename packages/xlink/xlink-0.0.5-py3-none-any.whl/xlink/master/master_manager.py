import time
import traceback
import threading
from ..common import tools
from loguru import logger
from ..common.schedule_center import ScheduleCenter


class MasterManager(threading.Thread):
    """
    MasterManager负责对ScheduleCenter单例进行治理
    Master以线程形式运行。
    Master作用：
    1 监控Master的绑定Worker是否正常接收任务和心跳，如果不正常，则重新分配；
    2 监控Master是否有需要重新分配的任务，有的话则重新分配；
    3 监控Master的mapping关系是否与Worker的mapping关系一致，如果不一致，告警（理论上不应该长时间存在这种情况）；
    """

    def __init__(self, schedule_center: ScheduleCenter, schedule_queue, heartbeats_timeout, batch_num=10000):
        threading.Thread.__init__(self)
        self._schedule_center = schedule_center
        self._schedule_queue = schedule_queue
        self._heartbeats_timeout = heartbeats_timeout
        self._batch_num = batch_num
        self._is_active = True
        self.daemon = True

    def run_once(self, now=None):
        timeout_address_set = self._step1_1_get_timeout_slave_address_set(now)
        self._step1_2_unbind_timeout_slave_address_set(timeout_address_set)
        added_key_num = self._step2_1_add_need_schedule_key_set()
        self._step2_2_reallocate()
        return added_key_num

    def _step1_1_get_timeout_slave_address_set(self, now=None):
        if now is None:
            now = int(time.time())
        timeout_address_set = set()
        for _address, _timestamps, in self._schedule_center.slave_heartbeats().items():
            if now - _timestamps > self._heartbeats_timeout:
                timeout_address_set.add(_address)
        return timeout_address_set

    def _step1_2_unbind_timeout_slave_address_set(self, slave_address_set):
        for _address in slave_address_set:
            self.timeout_unbind(_address)
            logger.warning(f'timeout_unbind address: {_address}')

    def _step2_1_add_need_schedule_key_set(self):
        key_list = tools.getn_from_queue(self._schedule_queue, self._batch_num)
        if len(key_list) > 0:
            key_set = set(key_list)
            self._schedule_center.add_reallocate_keys(key_set)
            return len(key_list)
        return 0

    def _step2_2_reallocate(self):
        for key in self._schedule_center.reallocate_keys().copy():
            result = self._schedule_center.allocate(key)
            if result is True:
                self._schedule_center.reallocate_keys().remove(key)
                logger.debug(f'reallocate key: {key}, result = {result}')
                # logger.info(f'reallocate key: {key}, result = {result}')
            else:
                logger.error(f'reallocate key: {key}, result = {result}')
                time.sleep(1)

    def timeout_unbind(self, address):
        secret_key_store = self._schedule_center.secret_key_store()
        secret_key = secret_key_store[address]
        self._schedule_center.unbind(address, secret_key)

    def run(self):
        assert self._is_active is True
        while self._is_active:
            try:
                num = self.run_once(now=None)
                if num == 0:
                    time.sleep(1)
            except Exception as e:
                logger.error(f'{e}, {traceback.print_exc()}')
                time.sleep(3)
            finally:
                pass
