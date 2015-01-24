import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.blog.models import BlogCategory
from mezzanine.utils.sites import current_site_id

from website.jdpages.models import get_public_blogposts
from website.jdpages.models import Sidebar, SidebarElementWidget
from website.jdpages.views import BlogPostItem
from website.jdpages.views import create_sidebar_items


def sidebar(request):
    """
    Adds the sidebar elements to the context.
    """
    sidebar = Sidebar.objects.filter(site_id=current_site_id(), active=True)
    
    if sidebar.count() > 1:
        logger.info('More than one sidebar active.')
    
    if not sidebar.exists():
        return {}

    sidebar_elements = SidebarElementWidget.objects.filter(sidebar=sidebar)
    sidebar_items = create_sidebar_items(sidebar_elements)

    return {"sidebar_items": sidebar_items,}
