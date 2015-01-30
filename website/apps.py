from django.apps import AppConfig


class JDPagesConfig(AppConfig):
    name = 'website.jdpages'
    label = 'jdpages'
    verbose_name = "JD Pages"

    # noinspection PyUnresolvedReferences
    def ready(self):
        import website.jdpages.signals


class CoreConfig(AppConfig):
    name = 'website.core'
    label = 'jdcore'  # prevent name collision with mezzanine.core
    verbose_name = "Website Core"
