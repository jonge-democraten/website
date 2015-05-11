import logging
logger = logging.getLogger(__name__)

from django.contrib.sites.models import Site

from mezzanine.conf import settings

from website.jdpages.models import Sidebar
from website.jdpages.models import SidebarBannerWidget
from website.jdpages.models import SidebarBlogCategoryWidget
from website.jdpages.models import SidebarTwitterWidget
from website.jdpages.models import SidebarTabsWidget
from website.jdpages.models import SocialMediaButton
from website.jdpages.views import BannerSidebarItem
from website.jdpages.views import BlogCategorySidebarItem
from website.jdpages.views import SocialMediaButtonGroupItem
from website.jdpages.views import TwitterSidebarItem
from website.jdpages.views import TabsSidebarItem

from website.jdpages.views import get_homepage_header


def site_properties(request):
    main_site_url = '/'
    main_site = Site.objects.filter(id=1)
    if main_site.exists():
        main_site_url = main_site[0].domain

    properties = {
        "site_tagline": settings.SITE_TAGLINE,
        "main_site_url": main_site_url
    }
    return properties


def piwik(request):
    if hasattr(settings, 'PIWIK_URL') and settings.PIWIK_URL != '':
        return {"piwik_url": settings.PIWIK_URL, "piwik_site_id": settings.PIWIK_SITE_ID}
    else:
        return {}


def sidebar(request):
    """
    Adds the sidebar elements to the context.
    """
    current_sidebars = Sidebar.objects.filter()

    if not current_sidebars.exists():
        return {}

    if current_sidebars.count() > 1:
        assert False  # there should never be more than one sidebar per site

    sidebar_items = []
    blogcategory_widgets = SidebarBlogCategoryWidget.objects.filter(sidebar=current_sidebars)
    for widget in blogcategory_widgets:
        item = BlogCategorySidebarItem(widget.blog_category)
        item.title = widget.title
        sidebar_items.append(item)

    tabs_widgets = SidebarTabsWidget.objects.filter(sidebar=current_sidebars, active=True)
    for widget in tabs_widgets:
        item = TabsSidebarItem()
        item.title = "Tabs"
        sidebar_items.append(item)

    twitter_widgets = SidebarTwitterWidget.objects.filter(sidebar=current_sidebars, active=True)
    for widget in twitter_widgets:
        item = TwitterSidebarItem()
        item.title = "Twitter"
        sidebar_items.append(item)

    banner_widgets = SidebarBannerWidget.objects.filter(active=True)
    for widget in banner_widgets:
        item = BannerSidebarItem(widget)
        item.title = widget.title
        sidebar_items.append(item)

    buttons = SocialMediaButton.objects.filter(sidebar=current_sidebars)
    if buttons:
        item = SocialMediaButtonGroupItem(buttons)
        sidebar_items.append(item)

    return {"sidebar_items": sidebar_items}


def homepage_header(request):
    return {"homepage_header": get_homepage_header()}
