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
    
    try:
        sidebar_blog_category = BlogCategory.objects.get(title=settings.SIDEBAR_BLOG)
    except BlogCategory.DoesNotExist:
        return {}  # the blog category may not exist
    sidebar_blog_posts = get_public_blogposts(sidebar_blog_category)
    sidebar_blogpost = sidebar_blog_posts.last()
    if not sidebar_blogpost:
        return {}
    blogpost_info = BlogPostItem(sidebar_blogpost)

    sidebar_elements = SidebarElementWidget.objects.filter(sidebar=sidebar)
    sidebar_items = create_sidebar_items(sidebar_elements)

    return {"sidebar_blogpost": blogpost_info,
            "sidebar_items": sidebar_items,}
