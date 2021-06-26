from lxd.apps import client


def create(name, description, is_vm):
    if is_vm:
        vm_or_container = "virtual-machine"
    else:
        vm_or_container = "container"

    config = {
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
        "type": f"{vm_or_container}",
    }

    client.instances.create(config, wait=True)
