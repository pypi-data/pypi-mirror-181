import time
import uuid
import traceback
import threading
from queue import Queue
from ..common import tools
from loguru import logger

DEFAULT_KPI = {
    'cpu_count': 4,
    'cpu_count_logical': 8,
    'cpu_percent': 0.0,
    'mem_total': 8,
    'mem_used': 5,
    'mem_free': 2,
    'mem_percent': 0.0,
    'disk_percent': 0.0,
}

lock = threading.Lock()


class ScheduleCenter:
    """
    ScheduleCenter必须是单例
    """

    _slave_queue_bindings = {}  # {address1: Queue1, address2: Queue2, ...}
    _key_slave_mappings = {}  # {key1: address2, key2: address3, ...}
    _slave_keys_mappings = {}  # {address1: {key1, key2, ...}, address2: {key11, key12, ...}, ...}
    """
    example:
    kpi dict = {
        'cpu_count': 4,
        'cpu_count_logical': 8,
        'cpu_percent': 0.2,
        'mem_total': 8,
        'mem_used': 5,
        'mem_free': 2,
        'mem_percent': 0.9,
        'disk_percent': 0.2,
    }
    """
    _slave_kpi_mappings = {}  # {address1: {[kpi dict1]}, address2: {[kpi dict2]}}
    _secret_key_store = {}  # {address1: secret_key2, address2: secret_key3, ...}
    _checksum_store = {}  # {address1: checksum1, address2: checksum2, ...}
    _slave_heartbeats = {}  # {address1: heartbeat_ts1, address2: heartbeat_ts2, ...}
    _reallocate_keys = set()  # {key1, key2, ..., keyn}

    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance of class already exits
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, *args, **kwargs):
        if self._initialized:
            return
        # set the attribute to `True` to not initialize again
        self._initialized = True

    def slave_heartbeats(self):
        # 仅供Master使用
        return self._slave_heartbeats

    def reallocate_keys(self):
        # 仅供Master使用
        return self._reallocate_keys

    def secret_key_store(self):
        # 仅供Master使用
        return self._secret_key_store

    def checksum_store(self):
        # 仅供Master使用
        return self._checksum_store

    def add_reallocate_keys(self, key_set):
        # 仅供Master使用
        self._reallocate_keys |= key_set

    def bind(self, address, reported_kpi=None, now=None):
        # 仅供Worker在初始化时使用
        """
        绑定，各个Worker初始化时调用ScheduleCenter的这个方法，用于告诉ScheduleCenter，自己可以接任务了；
        同时ScheduleCenter记录Worker和队列的绑定关系
        """
        if now is None:
            now = int(time.time())
        if reported_kpi is None:
            reported_kpi = DEFAULT_KPI
        try:
            lock.acquire()
            if address in self._slave_queue_bindings:
                return 100, f'address: {address} already in bindings'
            secret_key = uuid.uuid4().hex
            # 保存secret key
            self._secret_key_store[address] = secret_key
            # 对该address生成新Queue
            self._slave_queue_bindings[address] = Queue()
            # 更新心跳
            self._slave_heartbeats[address] = now
            # 默认kpi百分比指标为0
            self._slave_kpi_mappings[address] = reported_kpi
            # 初始化空列表
            self._slave_keys_mappings[address] = set()
            # 初始化checksum为0
            self._checksum_store[address] = 0
            return 200, secret_key
        finally:
            lock.release()

    def _route_address(self, slave_key_limit=10000):
        lowest_avg = 100.0
        most_free_address = None
        for _address, _kpi in self._slave_kpi_mappings.items():
            cpu_percent = _kpi['cpu_percent']
            mem_percent = _kpi['mem_percent']
            disk_percent = _kpi['disk_percent']
            avg_percent = (cpu_percent + mem_percent + disk_percent) / 3
            if avg_percent <= lowest_avg:
                slave_key_set_num = len(self._slave_keys_mappings[_address])
                if slave_key_set_num < slave_key_limit:
                    lowest_avg = avg_percent
                    most_free_address = _address
        return most_free_address

    def allocate(self, key, address=None):
        # 仅供Master使用，用于给slave分配schedule的key
        try:
            lock.acquire()
            if address is None:
                # 先检查在不在已分配的slave中
                address = self._key_slave_mappings.get(key, None)
            if address is None:
                address = self._route_address()
            if address is None:
                logger.error(f'no enough slave workers!!!')
                return False
            self._key_slave_mappings[key] = address
            slave_key_set = self._slave_keys_mappings[address]
            slave_key_set.add(key)
            last_checksum = self._checksum_store[address]
            new_checksum = last_checksum + int.from_bytes(str.encode(key), byteorder='little')
            self._checksum_store[address] = new_checksum
            # 把key推到对应的queue
            queue = self._slave_queue_bindings[address]
            queue.put(key)
            logger.debug(f'put key: {key}')
            return True
        finally:
            lock.release()

    def take(self, address, secret_key, checksum, reported_kpi, batch_num=1000, now=None):
        # 仅供Worker使用
        if now is None:
            now = int(time.time())
        """
        接消息（任务），Worker调用该方法接收消息，消息类型包含任务和心跳
        """
        try:
            store_key = self._secret_key_store.get(address, None)
            if store_key is None:
                return 403, f'your address: {address} not in store'
            if store_key != secret_key:
                return 401, f'your address: {address} secret_key: {secret_key} not match'
            store_checksum = self._checksum_store.get(address, None)
            if store_checksum is None:
                return 403, f'your address: {address} not in checksum store'
            code = 200
            if store_checksum != checksum:
                code = 300
                # return 401, f'your address: {address} checksum: {checksum} not match'
                logger.warning(f'your address: {address} checksum: {checksum} not match store_checksum: {store_checksum}')

            # 更新心跳
            self._slave_heartbeats[address] = now
            # 更新KPI
            self._slave_kpi_mappings[address] = reported_kpi
            address_queue = self._slave_queue_bindings[address]
            msg_list = tools.getn_from_queue(address_queue, batch_num)
            return code, msg_list
        except Exception as e:
            logger.error(f'{e}, {traceback.print_exc()}')
            return 404, f'exception: {e}'

    def unbind(self, address, secret_key):
        # Worker退出时或者Master检测超时后调用
        """
        解除绑定，Worker或定时检测程序调用该方法解除绑定，Master则清除绑定关系，并把原本该Worker的任务分发给其他Worker
        """
        try:
            lock.acquire()
            store_key = self._secret_key_store.get(address, None)
            if store_key is None:
                return 403, f'your address: {address} not in store'
            if store_key != secret_key:
                return 401, f'your address: {address} secret_key: {secret_key} not match'
            # 遍历key所在slave的address
            for _key, _address in self._key_slave_mappings.copy().items():
                if _address == address:
                    # time1 = time.time()
                    self._reallocate_keys.add(_key)
                    # time2 = time.time()
                    # print(f'_reallocate_keys add use time = {time2 - time1}')
                    del self._key_slave_mappings[_key]
                    # time3 = time.time()
                    # print(f'_key_slave_mappings del use time = {time3 - time2}')
            # 删除slave对应queue的绑定关系
            del self._slave_queue_bindings[address]
            # 删除slave的对应secret key的存储
            del self._secret_key_store[address]
            # 删除slave的对应checksum的存储
            del self._checksum_store[address]
            # 删除slave包含keys列表的映射关系
            del self._slave_keys_mappings[address]
            del self._slave_kpi_mappings[address]
            del self._slave_heartbeats[address]
        except Exception as e:
            logger.critical(f'{e}, {traceback.print_exc()}')
        finally:
            lock.release()
