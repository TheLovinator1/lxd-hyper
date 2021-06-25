from lxd.apps import client


def create(name, description, is_vm):
    if is_vm:
        vm_or_container = "virtual-machine"
    else:
        vm_or_container = "container"

    config = {
        "architecture": "",
        "config": {},
        "devices": {},
        "ephemeral": False,
        "profiles": None,
        "stateful": False,
        "description": f"{description}",
        "name": f"{name}",
        "source": {
            "type": "image",
            "certificate": "",
            "alias": "20.04",
            "server": "https://cloud-images.ubuntu.com/releases",
            "protocol": "simplestreams",
            "mode": "pull",
        },
        "instance_type": "",
        "type": f"{vm_or_container}",
    }

    client.instances.create(config, wait=True)
