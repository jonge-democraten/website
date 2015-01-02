
from django.apps import AppConfig

class JDPages(AppConfig):
    name = 'website.jdpages'
    label = 'jdpages'
    verbose_name = "JD Pages"
    
    def ready(self):
        import jdpages.signals 