import logging
logger = logging.getLogger(__name__)

from mezzanine.utils.sites import current_site_id

from website.jdpages.models import Sidebar, SidebarBlogCategoryWidget, SidebarTwitterWidget, SidebarBannerWidget
from website.jdpages.models import SocialMediaButton
from website.jdpages.views import BlogCategorySidebarItem, TwitterSidebarItem, BannerSidebarItem
from website.jdpages.views import SocialMediaButtonGroupItem

def sidebar(request):
    """
    Adds the sidebar elements to the context.
    """
    current_sidebars = Sidebar.objects.filter(site_id=current_site_id(), active=True)

    if not current_sidebars.exists():
        return {}

    if current_sidebars.count() > 1:
        logger.info('More than one sidebar active.')

    sidebar_items = []
    blogcategory_widgets = SidebarBlogCategoryWidget.objects.filter(sidebar=current_sidebars)
    for widget in blogcategory_widgets:
        item = BlogCategorySidebarItem(widget.blog_category)
        item.title = widget.title
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

    return {"sidebar_items": sidebar_items,}
