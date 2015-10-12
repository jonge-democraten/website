from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    def handle(self, *args, **options):
        site = Site.objects.get()
        site.domain = 'website.jongedemocraten.nl'
        site.name = 'Landelijk'
        site.save()
