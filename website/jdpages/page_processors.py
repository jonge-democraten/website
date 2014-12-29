import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.page_processors import processor_for

from .models import JDPage


@processor_for(JDPage)
@processor_for(JDHomePage)
def add_sidebar_blog_info(request, page):
    logger.warning(page.title)
    sidebar_blog_category = BlogCategory.objects.get(id=1)
    sidebar_blog_posts = BlogPost.objects.all().filter(categories=sidebar_blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    logger.warning(sidebar_blog_posts)
    return {"sidebar_blog_post": sidebar_blog_posts.last()}