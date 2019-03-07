from django.apps import AppConfig
# see more about app configration, https://docs.djangoproject.com/en/2.0/ref/applications/

class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
#         import signal handlers so that signals will be imported each time when images app is loaded
        import images.signals
