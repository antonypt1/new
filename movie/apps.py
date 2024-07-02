from django.apps import AppConfig
from django.apps import AppConfig


class MovieConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie'


class YourAppConfig(AppConfig):
    name = 'yourapp'

    def ready(self):
        import yourapp.signals
