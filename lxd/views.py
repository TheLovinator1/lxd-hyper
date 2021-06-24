from lxd.apps import client
from django.shortcuts import render

def index(request):
    container_list = client.containers.all()
    context = {
        "container_list": container_list,
        "firewall": client.host_info['environment']['firewall'],
        "kernel_version": client.host_info['environment']['kernel_version'],
        "server_name": client.host_info['environment']['server_name'],
        "lxd_version": client.host_info['environment']['server_version'],
        "os_name": client.host_info['environment']['os_name'],
        "storage": client.host_info['environment']['storage'],
        "storage_version": client.host_info['environment']['storage_version'],

    }
    return render(request, "lxd/index.html", context)


def about(request):
    container_list = client.containers.all()
    context = {
        "container_list": container_list,
    }
    return render(request, "lxd/about.html", context)


def container_detail(request, container_name):
    # FIXME: Add support for 404
    container_list = client.containers.all()
    for container in container_list:
        if container.name == container_name:
            context = {
                "container_list": container_list,
                "container": container,
            }
            return render(request, "lxd/detail.html", context)


def list_images(request):
    images_list = client.images.all()
    container_list = client.containers.all()
    context = {
        "container_list": container_list,
        "images_list": images_list,
    }
    return render(request, "lxd/images.html", context)


def image_detail(request, image_fingerprint):
    # FIXME: Add support for 404
    container_list = client.containers.all()
    image_list = client.images.all()
    for image in image_list:
        if image.fingerprint == image_fingerprint:
            context = {
                "container_list": container_list,
                "image": image,
            }
            return render(request, "lxd/image_detail.html", context)


def list_storage(request):
    container_list = client.containers.all()
    storage_pools = client.storage_pools.all()
    context = {
        "container_list": container_list,
        "storage_pools": storage_pools,
    }
    return render(request, "lxd/storage.html", context)


def storage_detail(request, storage_name: str):
    container_list = client.containers.all()
    storage_pools = client.storage_pools.all()
    if client.storage_pools.exists(storage_name):
        storage = client.storage_pools.get(storage_name)
        volumes = storage.volumes.all()
        context = {
            "container_list": container_list,
            "storage_pools": storage_pools,
            "volumes": volumes,
            "storage": storage,
            "storage_size": storage.config['size'], # Size of the storage pool in bytes
            "storage_source": storage.config['source'], # Path to block device, loop file or filesystem entry
            "storage_zfs_name": storage.config['zfs.pool_name'], # Name of the zpool
        }
        return render(request, "lxd/storage_detail.html", context)
    else:
        return "404 - No storage pool with that name."  # TODO: Make sexier
