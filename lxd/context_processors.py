import psutil
from lxd.apps import client


def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8KB'
    # >>> bytes2human(100001221)
    # '95.4MB'
    symbols = ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n


def psutil_stats(request):
    """Top right stats, memory and cpu usage"""
    cpu_usage = psutil.cpu_percent(interval=None)
    mem_used = psutil.virtual_memory().used
    mem_total = psutil.virtual_memory().total
    disk_usage = psutil.disk_usage("/var/lib/lxd/")

    loadavg = psutil.getloadavg()
    return {
        "disk_total": bytes2human(disk_usage.total),
        "disk_used": bytes2human(disk_usage.used),
        "disk_free": bytes2human(disk_usage.free),
        "disk_percent": disk_usage.percent,
        "cpu_usage": cpu_usage,
        "mem_used": bytes2human(mem_used),
        "mem_total": bytes2human(mem_total),
        "loadavg": loadavg,
    }


def sidebar(request):
    """Sidebar, containers and VMs"""
    container_list = client.containers.all()
    vm_list = client.virtual_machines.all()

    return {
        "container_list": container_list,
        "vm_list": vm_list,
    }
