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