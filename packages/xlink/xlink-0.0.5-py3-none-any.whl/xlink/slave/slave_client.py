import time
import traceback
import socket
from ..common.tools import get_kpi
from loguru import logger


class SlaveClient():

    def __init__(self, register_manager):
        """
        SlaveClient是对ScheduleCenter可用方法的封装，register_manager相当于schedule_center的代理
        """
        self._register_manager = register_manager
        self._address = None
        self._secret_key = None

    def bind(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        address_suffix = str(int(time.time() * 1000))[-9:]
        self._address = f'{hostname}-{ip_address}-{address_suffix}'
        print(f'bind address: {self._address}')
        _current_kpi = get_kpi()
        code, result = self._register_manager.get_schedule_center().bind(self._address, _current_kpi)
        if code != 200:
            raise Exception(f'exception when bind schedule center, code = {code}, result = {result}')
        self._secret_key = result

    def take(self, checksum, batch_num=2):
        _current_kpi = get_kpi()
        logger.debug(f'kpi = {_current_kpi}')
        result = self._register_manager.get_schedule_center().take(self._address, self._secret_key, checksum, _current_kpi, batch_num=batch_num, now=None)
        return result

    def reconnect(self):
        self._register_manager.reconnect()
