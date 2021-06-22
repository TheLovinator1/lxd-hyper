from django.urls import path

from . import views

urlpatterns = [
    # /
    path("", views.index, name="index"),
    # /about/
    path("about/", views.about, name="about"),
    # /container/neat-emu/
    path("container/<str:container_name>/", views.container_detail, name="container_detail"),
    # /images/
    path("images/", views.list_images, name="list_images"),
    # /image/ade188b16e5e719b73c14b5c19e7e65b8a15cf6f388be0bdb058012256b48a1e/
    path("image/<str:image_fingerprint>/", views.image_detail, name="image_detail"),
    # /storage/
    path("storage/", views.list_storage, name="list_storage"),
    # /storage/default/
    path("storage/<str:storage_name>/", views.storage_detail, name="storage_detail"),
]
