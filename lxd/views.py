from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from lxd.apps import client
from lxd.bytes2human import bytes2human
from lxd.forms import CreateInstanceForm, CreateNetworkForm, CreateNewSnapshotForm

# TODO: Disable virtual machine stuff if QEMU is not installed.


def index(request):
    """Index page.

    Returns:
        /index.html (or /)
    """
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


def container_detail(request, container_name):
    """Details about containers.

    Returns:
        /container_detail.html (or /container/<str:container_name>/)
    """
    # FIXME: Add support for 404
    container = client.containers.get(container_name)
    state = container.state()
    context = {
        "container": container,
        "image_architecture": container.config["image.architecture"],
        "image_description": container.config["image.description"],
        "image_os": container.config["image.os"],
        "image_release": container.config["image.release"],
        "image_serial": container.config["image.serial"],
        "image_type": container.config["image.type"],
        "memory_usage": bytes2human(state.memory["usage"]),
        "memory_usage_peak": bytes2human(state.memory["usage_peak"]),
        "memory_swap_usage": bytes2human(state.memory["swap_usage"]),
        "memory_swap_usage_peak": bytes2human(state.memory["swap_usage_peak"]),
        # "root_disk_usage": bytes2human(state.disk["root"]["usage"]), #FIXME: Does not work with btrfs
        "cpu_usage": state.cpu["usage"],
    }
    if container.status == "Running":
        add_extra_context_if_running(context, state)
    return render(request, "lxd/container_detail.html", context)


def add_extra_context_if_running(context, state):
    """Add extra context to container_detail page if the container is running.

    This is information that can only be accessed when the container is live.
    """
    context["network_ipv4_address"] = state.network["eth0"]["addresses"][0]["address"]
    context["network_ipv4_netmask"] = state.network["eth0"]["addresses"][0]["netmask"]
    context["network_ipv4_scope"] = state.network["eth0"]["addresses"][0]["scope"]
    context["network_ipv6_address"] = state.network["eth0"]["addresses"][1]["address"]
    context["network_ipv6_netmask"] = state.network["eth0"]["addresses"][1]["netmask"]
    context["network_ipv6_scope"] = state.network["eth0"]["addresses"][1]["scope"]
    context["network_bytes_received"] = bytes2human(state.network["eth0"]["counters"]["bytes_received"])
    context["network_bytes_sent"] = bytes2human(state.network["eth0"]["counters"]["bytes_sent"])
    context["network_packets_received"] = state.network["eth0"]["counters"]["packets_received"]
    context["network_packets_sent"] = state.network["eth0"]["counters"]["packets_sent"]
    context["network_hwaddr"] = state.network["eth0"]["hwaddr"]
    context["network_host_name"] = state.network["eth0"]["host_name"]
    context["network_mtu"] = state.network["eth0"]["mtu"]
    context["network_state"] = state.network["eth0"]["state"]
    context["network_type"] = state.network["eth0"]["type"]


def instance_start(request, instance_name):
    """Check if the instance is running and if not, start it."""
    instance = client.instances.get(instance_name)
    if instance.state == "Running":
        print(f"{instance_name} is already running")
    else:
        print(f"Starting {instance_name}")
        instance.start(wait=True)

    return redirect("container_detail", instance_name)


def instance_stop(request, instance_name):
    """Check if the instance is stopped and if not, stop it."""
    instance = client.instances.get(instance_name)
    if instance.state == "Stopped":
        print(f"{instance_name} is already stopped")
    else:
        print(f"Stopping {instance_name}")
        instance.stop(wait=True)

    return redirect("container_detail", instance_name)


def instance_restart(request, instance_name):
    """Restart if instance is running."""
    instance = client.instances.get(instance_name)
    if instance.state == "Running":
        print(f"Restarting {instance_name}")
        instance.restart(wait=True)
    else:
        print("Instance needs to be running")

    return redirect("container_detail", instance_name)


def instance_suspend(request, instance_name):
    """Suspend running instance. Also called freeze."""
    instance = client.instances.get(instance_name)
    if instance.state != "Running":
        if instance.state == "Frozen":
            print(f"{instance_name} is already suspended")

        print(f"Suspending {instance_name}")
        instance.freeze(wait=True)
    else:
        print("Instance is not running")

    return redirect("container_detail", instance_name)


def instance_resume(request, instance_name):
    """Resume instance if suspended. Also called unfreeze."""
    instance = client.instances.get(instance_name)
    if instance.state != "Frozen":
        if instance.state == "Running":
            print(f"{instance_name} is already resumed")
        print(f"Resuming {instance_name}")
        instance.unfreeze(wait=True)
    else:
        print("Instance needs to be suspended")

    return redirect("container_detail", instance_name)


def vm_detail(request, vm_name: str):
    """Detail page for virtual machines.

    Args:
        vm_name (str): Virtual machine name.

    Returns:
        /vm_detail.html (or /vm/<str:vm_name>/)
    """
    # FIXME: Add support for 404
    vm = client.virtual_machines.get(vm_name)
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
    """List downloaded images.

    Returns:
        /images.html (or /images/)
    """
    context = {
        "images_list": client.images.all(),
    }
    return render(request, "lxd/images.html", context)


def image_detail(request, image_fingerprint: str):
    """Details about images.

    Args:
        image_fingerprint (str):Sha2 hash of the image data itself. This unique key identifies the image.

    Returns:
        /image_detail.html (or /image/<str:image_fingerprint>/)
    """
    # FIXME: Add support for 404
    context = {"image": client.images.get(image_fingerprint)}
    return render(request, "lxd/image_detail.html", context)


def list_networks(request):
    """List networks available to LXD.

    Returns:
        /networks.html (or /networks/)
    """
    context = {"networks_list": client.networks.all()}
    return render(request, "lxd/networks.html", context)


def network_detail(request, network_name: str):
    """Details about network.

    Args:
        network_name (str): The name of the network.

    Returns:
        /networks.html (or /network/<str:network_name>/)
    """
    # FIXME: Add support for 404
    network = client.networks.get(network_name)

    context = {
        "network": network,
    }

    if network.config:
        if network.config["ipv4.address"]:
            context["ipv4_address"] = network.config["ipv4.address"]
        if network.config["ipv4.nat"]:
            context["ipv4_nat"] = network.config["ipv4.nat"]
        if network.config["ipv6.address"]:
            context["ipv6_address"] = network.config["ipv6.address"]  # TODO: Check if ipv6_nat exists
    return render(request, "lxd/network_detail.html", context)


def list_storage(request):
    """List storage pools.

    Returns:
        /storage.html (or /storage_pools/)
    """
    storage_pools = client.storage_pools.all()
    context = {"storage_pools": storage_pools}
    return render(request, "lxd/storage.html", context)


def storage_detail(request, storage_name: str):
    """Details about storage pools.

    Args:
        storage_name (str): Storage pool name.

    Returns:
        /storage_detail.html (or /storage/<str:storage_name>/)
    """
    # TODO: Add ZFS, Btrfs things
    storage = client.storage_pools.get(storage_name)
    context = {
        "volumes": storage.volumes.all(),
        "storage": storage,
    }
    return render(request, "lxd/storage_detail.html", context)


def list_profiles(request):
    """List profiles.

    Returns:
        /profiles.html (or /profiles/)
    """
    context = {
        "profiles_list": client.profiles.all(),
    }
    return render(request, "lxd/profiles.html", context)


def profile_detail(request, profile_name: str):
    """Details about profiles.

    Args:
        profile_name (str): Profile name.

    Returns:
        /profile_detail.html (or /profile/<str:profile_name>/)
    """
    context = {
        "profile": client.profiles.get(profile_name),
    }
    return render(request, "lxd/profile_detail.html", context)


def list_projects(request):
    """List projects. A project holds it own set of instances and may have its own images and profiles.

    Returns:
        /projects.html (or /projects/)
    """
    context = {"projects_list": client.projects.all()}
    return render(request, "lxd/projects.html", context)


def project_detail(request, project_name: str):
    """Details about projects.

    Args:
        project_name (str): Name of project.

    Returns:
        /project_detail.html (or /project/<str:project_name>/)
    """
    project = client.projects.get(project_name)
    context = {
        "project": project,
        "features_images": project.config["features.images"],
        "features_networks": project.config["features.networks"],
        "features_profiles": project.config["features.profiles"],
        "features_storage_volumes": project.config["features.storage.volumes"],
    }
    return render(request, "lxd/project_detail.html", context)


def list_certificates(request):
    """List certificates. Certificates are used to mange authentications in LXD.

    Returns:
        /certificates.html (or /certificates/)
    """
    context = {
        "certificates_list": client.certificates.all(),
    }
    return render(request, "lxd/certificates.html", context)


def create_instance(request):
    """Create new container or VM. You can add name, description and image.

    Returns:
        container_detail/vm_detail: Depending if you created a container or a virtual machine
        you will get sent to the detail page for the correct type.
    """
    if request.method == "POST":
        form = CreateInstanceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            image_alias = form.cleaned_data.get("image")
            is_vm = form.cleaned_data.get("is_vm")

            vm_or_container = "virtual-machine" if is_vm else "container"
            config = {
                "description": f"{description}",
                "name": f"{name}",
                "source": {
                    "type": "image",
                    "alias": f"{image_alias}",
                    "server": "https://images.linuxcontainers.org",
                    "protocol": "simplestreams",
                    "mode": "pull",
                },
                "type": f"{vm_or_container}",
            }

            client.instances.create(config, wait=True)

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
        "images_list": client.images.all(),
        "form": form,
    }

    return render(request, "lxd/create_instance.html", context)


def create_network(request):
    """Create a new network.

    Returns:
        /network_create.html (or /certificates/)
    """
    # TODO: Fails with "Failed clearing firewall: Failed clearing nftables rules for network: EOF"
    if request.method == "POST":
        form = CreateNetworkForm(request.POST)

        if form.is_valid():
            client.networks.create(
                form.cleaned_data.get("name"),
                description=form.cleaned_data.get("description"),
                type=form.cleaned_data.get("network_type"),
                config={},
                wait=True,
            )
            return HttpResponseRedirect(
                reverse("network_detail", kwargs={"network_name": form.cleaned_data.get("name")})
            )
    else:
        form = CreateNetworkForm()

    return render(
        request,
        "lxd/network_create.html",
        {"form": form},
    )


def instace_snapshots(request, instance_name: str):
    """List all snapshots for this instance.

    Args:
        instance_name (str): Container or VM name.

    Returns:
        /snapshots.html (or /snapshots/)
    """
    instance = client.instances.get(instance_name)
    context = {
        "snapshot_list": instance.snapshots.all(),
        "instance_name": instance_name,
    }
    return render(request, "lxd/snapshots.html", context)


def snapshot_create(request, instance_name: str):
    """Create new snapshot.

    Args:
        instance_name (str): Container or VM name.

    Returns:
        /container/<str:instance_name>/snapshot_create
    """
    instance = client.instances.get(instance_name)

    if request.method == "POST":
        form = CreateNewSnapshotForm(request.POST)

        if form.is_valid():
            instance.snapshots.create(
                form.cleaned_data.get("name"), stateful=form.cleaned_data.get("stateful"), wait=True
            )
            return HttpResponseRedirect(reverse("instace_snapshots", kwargs={"instance_name": instance_name}))
    else:
        form = CreateNewSnapshotForm()

    return render(
        request,
        "lxd/snapshot_create.html",
        {"form": form},
    )


def snapshot_detail(request, instance_name: str, snapshot_name: str):
    """Details about a snapshot.

    Returns:
        /snapshot_detail.html (or /container/<str:instance_name>/snapshot/<str:snapshot_name>)
    """
    # FIXME: Add support for 404
    instance = client.instances.get(instance_name)
    context = {
        "snapshot": instance.snapshots.get(snapshot_name),
        "instance_name": instance_name,
        "snapshot_name": snapshot_name,
    }

    return render(request, "lxd/snapshot_detail.html", context)


def snapshot_remove(request, instance_name: str, snapshot_name: str):
    """Remove snapshot.

    Args:
        instance_name (str): Container or VM name.
        snapshot_name (str): Snapshot name.

    Returns:
        /container/<str:instance_name>/snapshot/<str:snapshot_name>/remove
    """
    instance = client.instances.get(instance_name)
    snapshot = instance.snapshots.get(snapshot_name)
    snapshot.delete(wait=True)
    return HttpResponseRedirect(reverse("instace_snapshots", kwargs={"instance_name": instance_name}))
