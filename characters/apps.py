from django.apps import AppConfig


class CharactersConfig(AppConfig):
    name = 'characters'

    def ready(self):
        from . import signals  
