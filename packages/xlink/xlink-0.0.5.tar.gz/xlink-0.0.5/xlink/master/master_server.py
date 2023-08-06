import sys
import threading
from multiprocessing.managers import BaseManager
from ..common.schedule_center import ScheduleCenter
from ..master.master_manager import MasterManager
from loguru import logger
from ..master.master_api import app
from ..common.protocol import DEFAULT_SCHEDULE_CENTER_NAME


class ScheduleManager(BaseManager):
    pass


class MasterServer():

    def __init__(self, api_port, queue_port, auth_key, log_level='INFO'):
        self._api_port = api_port
        self._queue_port = queue_port
        self._auth_key = auth_key
        logger.remove()
        logger.add(sys.stderr, level=log_level)

    def run(self, schedule_queue, heartbeats_timeout=190):
        schedule_center = ScheduleCenter()
        mst = MasterManager(schedule_center, schedule_queue, heartbeats_timeout)
        mst.start()
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=self._api_port, debug=True, use_reloader=False), daemon=True).start()
        ScheduleManager.register(DEFAULT_SCHEDULE_CENTER_NAME, ScheduleCenter)
        m = ScheduleManager(address=('0.0.0.0', self._queue_port), authkey=self._auth_key)
        s = m.get_server()
        s.serve_forever()