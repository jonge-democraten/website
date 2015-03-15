import logging
logger = logging.getLogger(__name__)

from website.jdpages.models import Sidebar
from website.jdpages.models import SidebarBannerWidget
from website.jdpages.models import SidebarBlogCategoryWidget
from website.jdpages.models import SidebarTwitterWidget
from website.jdpages.models import SocialMediaButton
from website.jdpages.views import BannerSidebarItem
from website.jdpages.views import BlogCategorySidebarItem
from website.jdpages.views import SocialMediaButtonGroupItem
from website.jdpages.views import TwitterSidebarItem


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
