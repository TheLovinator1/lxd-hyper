from django.urls import path

from . import views

urlpatterns = [
    # /
    path(
        "",
        views.index,
        name="index",
    ),
    # /about/
    path(
        "about/",
        views.about,
        name="about",
    ),
    # /container/neat-emu/
    path(
        "container/<str:container_name>/",
        views.container_detail,
        name="container_detail",
    ),
    # /vm/ubuntuvm/
    path(
        "vm/<str:vm_name>/",
        views.vm_detail,
        name="vm_detail",
    ),
    # /images/
    path(
        "images/",
        views.list_images,
        name="list_images",
    ),
    # /image/ade188b16e5e719b73c14b5c19e7e65b8a15cf6f388be0bdb058012256b48a1e/
    path(
        "image/<str:image_fingerprint>/",
        views.image_detail,
        name="image_detail",
    ),
    # /storage_pools/
    path(
        "storage_pools/",
        views.list_storage,
        name="list_storage",
    ),
    # /storage/default/
    path(
        "storage/<str:storage_name>/",
        views.storage_detail,
        name="storage_detail",
    ),
    # /networks/
    path(
        "networks/",
        views.list_networks,
        name="list_networks",
    ),
    # /network/lxdbr0/
    path(
        "network/<str:network_name>/",
        views.network_detail,
        name="network_detail",
    ),
    # /profiles/
    path(
        "profiles/",
        views.list_profiles,
        name="list_profiles",
    ),
    # /profile/default/
    path(
        "profile/<str:profile_name>/",
        views.profile_detail,
        name="profile_detail",
    ),
    # /projects/
    path(
        "projects/",
        views.list_projects,
        name="list_projects",
    ),
    # /project/default/
    path(
        "project/<str:project_name>/",
        views.project_detail,
        name="project_detail",
    ),
    # /certificates/
    path(
        "certificates/",
        views.list_certificates,
        name="list_certificates",
    ),
    # /create_instance/
    path(
        "create_instance/",
        views.create_instance,
        name="create_instance",
    ),
    # /create_network/
    path(
        "create_network/",
        views.create_network,
        name="create_network",
    ),
    # /container/neat-emu/start
    path(
        "container/<str:container_name>/start/",
        views.instance_start,
        name="instance_start",
    ),
    # /container/neat-emu/stop
    path(
        "container/<str:container_name>/stop/",
        views.instance_stop,
        name="instance_stop",
    ),
]
