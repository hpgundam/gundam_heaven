from django.apps import AppConfig


class GundamHeavenConfig(AppConfig):
    name = 'gundam_heaven'

    def ready(self):
        import gundam_heaven.signals
