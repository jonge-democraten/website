import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

from website.utils.containers import BlogPostItem


def page(request):
    """
    Adds the sidebar blogpost info to the context.
    """
    try: 
        sidebar_blog_category = BlogCategory.objects.get(title=settings.SIDEBAR_BLOG)
    except BlogCategory.DoesNotExist:
        return {} # the blog category may not exist
    sidebar_blog_posts = BlogPost.objects.all().filter(categories=sidebar_blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    sidebar_blogpost = sidebar_blog_posts.last()
    if not sidebar_blogpost:
        return {}
    blogpost_info = BlogPostItem(sidebar_blogpost)
    return {"sidebar_blogpost": blogpost_info}
