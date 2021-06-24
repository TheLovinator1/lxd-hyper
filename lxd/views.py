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
                "image_architecture": container.config['image.architecture'],
                "image_description": container.config['image.description'],
                "image_os": container.config['image.os'],
                "image_release": container.config['image.release'],
                "image_serial": container.config['image.serial'],
                "image_type": container.config['image.type'],
                "image_variant": container.config['image.variant'],
                "volatile_base_image": container.config['volatile.base_image'],
                "volatile_eth0_hwaddr": container.config['volatile.eth0.hwaddr'],
                "volatile_idmap_base": container.config['volatile.idmap.base'],
                "volatile_idmap_current": container.config['volatile.idmap.current'],
                "volatile_idmap_next": container.config['volatile.idmap.next'],
                "volatile_last_state_idmap": container.config['volatile.last_state.idmap'],
                "volatile_last_state_power": container.config['volatile.last_state.power'],
                "volatile_uuid": container.config['volatile.uuid'],
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


def list_networks(request):
    networks_list = client.networks.all()
    container_list = client.containers.all()
    context = {
        "container_list": container_list,
        "networks_list": networks_list,
    }
    return render(request, "lxd/networks.html", context)


def network_detail(request, network_name):
    # FIXME: Add support for 404
    container_list = client.containers.all()
    networks_list = client.networks.all()
    for network in networks_list:
        if network.name == network_name:
            context = {
                "container_list": container_list,
                "network": network,
            }
            if network.config:
                if network.config['ipv4.address']:
                    context["ipv4_address"] = network.config['ipv4.address']
                if network.config['ipv4.nat']: 
                    context["ipv4_nat"] = network.config['ipv4.nat']
                if network.config['ipv6.address']:
                    context["ipv6_address"] =  network.config['ipv6.address'] # TODO: Check if ipv6_nat exists
            return render(request, "lxd/network_detail.html", context)

def list_storage(request):
    container_list = client.containers.all()
    storage_pools = client.storage_pools.all()
    context = {
        "container_list": container_list,
        "storage_pools": storage_pools,
    }
    return render(request, "lxd/storage.html", context)


def storage_detail(request, storage_name: str):
    # TODO: Add zfs.pool_name
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
        }
        return render(request, "lxd/storage_detail.html", context)
    else:
        return "404 - No storage pool with that name."  # TODO: Make sexier

def list_profiles(request):
    container_list = client.containers.all()
    profiles_list = client.profiles.all()
    context = {
        "container_list": container_list,
        "profiles_list": profiles_list,
    }
    return render(request, "lxd/profiles.html", context)


def profile_detail(request, profile_name: str):
    container_list = client.containers.all()
    profiles_list = client.profiles.all()
    if client.profiles.exists(profile_name):
        profile = client.profiles.get(profile_name)
        context = {
            "container_list": container_list,
            "profiles_list": profiles_list,
            "profile": profile,
        }
        return render(request, "lxd/profile_detail.html", context)
    else:
        return "404 - No profile with that name."  # TODO: Make sexier

def list_projects(request):
    container_list = client.containers.all()
    projects_list = client.projects.all()
    context = {
        "container_list": container_list,
        "projects_list": projects_list,
    }
    return render(request, "lxd/projects.html", context)


def project_detail(request, project_name: str):
    container_list = client.containers.all()
    projects_list = client.projects.all()
    if client.projects.exists(project_name):
        project = client.projects.get(project_name)
        context = {
            "container_list": container_list,
            "projects_list": projects_list,
            "project": project,
            "features_images": project.config['features.images'],
            "features_networks": project.config['features.networks'],
            "features_profiles": project.config['features.profiles'],
            "features_storage_volumes": project.config['features.storage.volumes'],
        }
        return render(request, "lxd/project_detail.html", context)
    else:
        return "404 - No project with that name."  # TODO: Make sexier


def list_certificates(request):
    container_list = client.containers.all()
    certificates_list = client.certificates.all()
    context = {
        "container_list": container_list,
        "certificates_list": certificates_list,
    }
    return render(request, "lxd/certificates.html", context)
