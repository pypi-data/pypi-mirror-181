import re
import time
import psutil
from queue import Empty


def getn_from_queue(queue, n, sleep_seconds=0.0001):
    """
    通用的在queue里面批量取n个值再返回，方便后续的批量操作
    """
    results = []
    try:
        while len(results) < n:
            results.append(queue.get(block=False))
    except Empty:
        time.sleep(sleep_seconds)
    return results


def get_kpi():
    # 查看cpu物理个数的信息
    cpu_count = psutil.cpu_count(logical=False)
    # CPU的使用率
    cpu_percent = psutil.cpu_percent()
    # 查看cpu逻辑个数的信息
    cpu_count_logical = psutil.cpu_count(logical=True)
    # 内存
    mem = psutil.virtual_memory()
    # 系统总计内存
    mem_total = float(mem.total) / 1024 / 1024 / 1024
    # 系统已经使用内存
    mem_used = float(mem.used) / 1024 / 1024 / 1024
    # 系统空闲内存
    mem_free = float(mem.free) / 1024 / 1024 / 1024
    mem_percent = mem[2]
    # 磁盘使用率
    disk_percent = psutil.disk_usage('/').percent
    return {
        'cpu_count': cpu_count,
        'cpu_count_logical': cpu_count_logical,
        'cpu_percent': cpu_percent,
        'mem_total': round(mem_total, 2),
        'mem_used': round(mem_used, 2),
        'mem_free': round(mem_free, 2),
        'mem_percent': mem_percent,
        'disk_percent': disk_percent,
    }


def validate_iso8601(str_val):
    """
    校验是不是iso8601的字符串时间
    """
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(str_val) is not None:
            return True
    except Exception:
        pass
    return False


def validate_utc_iso8601(str_val):
    """
    校验是不是iso8601的utc字符串时间
    """
    is_valid_iso8601 = validate_iso8601(str_val)
    is_utc = str_val[-5:] == '00:00'
    if is_valid_iso8601 and is_utc:
        return True
    return False
