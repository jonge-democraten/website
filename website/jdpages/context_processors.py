import logging
logger = logging.getLogger(__name__)

from django.contrib.sites.models import Site

from mezzanine.conf import settings

from website.jdpages.views import get_homepage_header


def site_properties(request):
    """ :returns: basic site properties """
    if not hasattr(request, '__main_site_url'):
        try:
            dom = Site.objects.values_list('domain', flat=True).get(pk=1)
            request.__main_site_url = 'http://' + dom
        except Site.DoesNotExist:
            return {}

    properties = {
        "site_tagline": settings.SITE_TAGLINE,
        "main_site_url": request.__main_site_url
    }
    return properties


def piwik(request):
    """ :returns: the the Piwik analytics URL and SITE_ID """
    if hasattr(settings, 'PIWIK_URL') and settings.PIWIK_URL != '':
        return {"piwik_url": settings.PIWIK_URL, "piwik_site_id": settings.PIWIK_SITE_ID}
    else:
        return {}


def homepage_header(request):
    if not hasattr(request, '__homepage_header'):
        request.__homepage_header = get_homepage_header()
    return {"homepage_header": request.__homepage_header}
