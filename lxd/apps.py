from django.apps import AppConfig
from pylxd import Client


class LxdConfig(AppConfig):
    """Metadata about for the django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "lxd"

    def ready(self):
        """Django runs this function on startup.

        We use it to instantiate the API client for pylxd.
        """
        global client  # TODO: Change this from a global to something better
        client = Client()
