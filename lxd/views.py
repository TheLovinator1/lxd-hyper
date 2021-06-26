from django.http import HttpResponseRedirect
from django.urls import reverse
from lxd.apps import client
from django.shortcuts import render
from lxd.forms import CreateInstanceForm
from lxd.create_instance import create


def index(request):

    context = {
        "firewall": client.host_info["environment"]["firewall"],
        "kernel_version": client.host_info["environment"]["kernel_version"],
        "server_name": client.host_info["environment"]["server_name"],
        "lxd_version": client.host_info["environment"]["server_version"],
        "os_name": client.host_info["environment"]["os_name"],
        "storage": client.host_info["environment"]["storage"],
        "storage_version": client.host_info["environment"]["storage_version"],
    }
    return render(request, "lxd/index.html", context)


def about(request):

    context = {}
    return render(request, "lxd/about.html", context)


def container_detail(request, container_name):
    # FIXME: Add support for 404
    container_list = client.containers.all()
    for container in container_list:
        if container.name == container_name:
            context = {
                "container": container,
                "image_architecture": container.config["image.architecture"],
                "image_description": container.config["image.description"],
                "image_os": container.config["image.os"],
                "image_release": container.config["image.release"],
                "image_serial": container.config["image.serial"],
                "image_type": container.config["image.type"],
            }
            return render(request, "lxd/container_detail.html", context)


def vm_detail(request, vm_name):
    # FIXME: Add support for 404
    vm_list = client.virtual_machines.all()
    for vm in vm_list:
        if vm.name == vm_name:
            context = {
                "vm": vm,
                "image_architecture": vm.config["image.architecture"],
                "image_description": vm.config["image.description"],
                "image_os": vm.config["image.os"],
                "image_release": vm.config["image.release"],
                "image_serial": vm.config["image.serial"],
                "image_type": vm.config["image.type"],
            }
            return render(request, "lxd/vm_detail.html", context)


def list_images(request):
    images_list = client.images.all()

    context = {
        "images_list": images_list,
    }
    return render(request, "lxd/images.html", context)


def image_detail(request, image_fingerprint):
    # FIXME: Add support for 404
    image_list = client.images.all()

    for image in image_list:
        if image.fingerprint == image_fingerprint:
            context = {
                "image": image,
            }
            return render(request, "lxd/image_detail.html", context)


def list_networks(request):
    networks_list = client.networks.all()
    context = {
        "networks_list": networks_list,
    }
    return render(request, "lxd/networks.html", context)


def network_detail(request, network_name):
    # FIXME: Add support for 404
    networks_list = client.networks.all()

    for network in networks_list:
        if network.name == network_name:
            context = {
                "network": network,
            }
            if network.config:
                if network.config["ipv4.address"]:
                    context["ipv4_address"] = network.config["ipv4.address"]
                if network.config["ipv4.nat"]:
                    context["ipv4_nat"] = network.config["ipv4.nat"]
                if network.config["ipv6.address"]:
                    context["ipv6_address"] = network.config[
                        "ipv6.address"
                    ]  # TODO: Check if ipv6_nat exists
            return render(request, "lxd/network_detail.html", context)


def list_storage(request):
    storage_pools = client.storage_pools.all()
    context = {
        "storage_pools": storage_pools,
    }
    return render(request, "lxd/storage.html", context)


def storage_detail(request, storage_name: str):
    # TODO: Add zfs.pool_name
    storage_pools = client.storage_pools.all()

    if client.storage_pools.exists(storage_name):
        storage = client.storage_pools.get(storage_name)
        volumes = storage.volumes.all()
        context = {
            "storage_pools": storage_pools,
            "volumes": volumes,
            "storage": storage,
        }
        return render(request, "lxd/storage_detail.html", context)
    else:
        return "404 - No storage pool with that name."  # TODO: Make sexier


def list_profiles(request):
    profiles_list = client.profiles.all()
    context = {
        "profiles_list": profiles_list,
    }
    return render(request, "lxd/profiles.html", context)


def profile_detail(request, profile_name: str):
    profiles_list = client.profiles.all()

    if client.profiles.exists(profile_name):
        profile = client.profiles.get(profile_name)
        context = {
            "profiles_list": profiles_list,
            "profile": profile,
        }
        return render(request, "lxd/profile_detail.html", context)
    else:
        return "404 - No profile with that name."  # TODO: Make sexier


def list_projects(request):
    projects_list = client.projects.all()
    context = {
        "projects_list": projects_list,
    }
    return render(request, "lxd/projects.html", context)


def project_detail(request, project_name: str):
    projects_list = client.projects.all()

    if client.projects.exists(project_name):
        project = client.projects.get(project_name)
        context = {
            "projects_list": projects_list,
            "project": project,
            "features_images": project.config["features.images"],
            "features_networks": project.config["features.networks"],
            "features_profiles": project.config["features.profiles"],
            "features_storage_volumes": project.config["features.storage.volumes"],
        }
        return render(request, "lxd/project_detail.html", context)
    else:
        return "404 - No project with that name."  # TODO: Make sexier


def list_certificates(request):
    certificates_list = client.certificates.all()
    context = {
        "certificates_list": certificates_list,
    }
    return render(request, "lxd/certificates.html", context)


def create_instance(request):
    images_list = client.images.all()

    if request.method == "POST":
        form = CreateInstanceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            is_vm = form.cleaned_data.get("is_vm")

            create(name, description, is_vm)
            if is_vm:
                return HttpResponseRedirect(
                    reverse(
                        "vm_detail", kwargs={"vm_name": name}
                    )  # FIXME: This does not work with auto generated names
                )
            else:
                return HttpResponseRedirect(
                    reverse(
                        "container_detail", kwargs={"container_name": name}
                    )  # FIXME: This does not work with auto generated names
                )
    else:
        form = CreateInstanceForm()

    context = {
        "images_list": images_list,
        "form": form,
    }

    return render(request, "lxd/create_instance.html", context)
