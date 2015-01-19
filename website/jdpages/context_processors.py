import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import get_public_blogposts
from website.jdpages.models import SidebarElementWidget
from website.jdpages.views import BlogPostItem


def sidebar(request):
    """
    Adds the sidebar elements to the context.
    """
    try:
        sidebar_blog_category = BlogCategory.objects.get(title=settings.SIDEBAR_BLOG)
    except BlogCategory.DoesNotExist:
        return {}  # the blog category may not exist
    sidebar_blog_posts = get_public_blogposts(sidebar_blog_category)
    sidebar_blogpost = sidebar_blog_posts.last()
    if not sidebar_blogpost:
        return {}
    blogpost_info = BlogPostItem(sidebar_blogpost)
    
    sidebar_elements = SidebarElementWidget.objects.all()
    sidebar_elements = SidebarElementWidget.add_items_to_widgets(sidebar_elements)

    return {"sidebar_blogpost": blogpost_info,
            "sidebar_elements": sidebar_elements,}
