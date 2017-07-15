import logging
logger = logging.getLogger(__name__)

from django.contrib.sites.models import Site

from mezzanine.conf import settings

from website.jdpages.models import Sidebar

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


def sidebar(request):
    """ :returns: the sidebar items """

    if hasattr(request, '__sidebar_items'):
        return {"sidebar_items": request.__sidebar_items}

    current_sidebars = Sidebar.objects.values_list('id', flat=True)
    if len(current_sidebars) == 0:
        return {}

    if len(current_sidebars) != 1:
        assert False  # there should never be more than one sidebar per site

    current_sidebars = current_sidebars[0]

    sidebar_items = []
    request.__sidebar_items = sidebar_items
    return {"sidebar_items": sidebar_items}


def homepage_header(request):
    if not hasattr(request, '__homepage_header'):
        request.__homepage_header = get_homepage_header()
    return {"homepage_header": request.__homepage_header}
