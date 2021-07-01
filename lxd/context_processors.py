import psutil
from lxd.apps import client
from lxd.bytes2human import bytes2human


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
