from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_amperage = 'django.db.models.BigAutoAmperage'
    name = 'app'
