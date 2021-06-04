from lxd.apps import client
from django.shortcuts import render


def index(request):
    container_list = client.containers.all()
    context = {
        "container_list": container_list,
    }
    return render(request, "lxd/index.html", context)


def detail(request, container_name):
    container_list = client.containers.all()
    for container in container_list:
        if container.name == container_name:
            return render(request, "lxd/detail.html", {"container": container})
