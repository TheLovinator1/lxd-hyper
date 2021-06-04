from django.apps import AppConfig
from pylxd import Client


class LxdConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lxd"

    def ready(self):
        global client
        client = Client()
