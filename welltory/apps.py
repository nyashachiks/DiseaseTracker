from django.apps import AppConfig


class WelltoryConfig(AppConfig):
    name = 'welltory'

    def ready(self):
        import welltory.signals
