import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.page_processors import processor_for

from .models import JDPage, JDHomePage


class BlogPostInfo():
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.content = strip_tags(blogpost.content)
        self.url = blogpost.get_absolute_url()


@processor_for(JDPage)
@processor_for(JDHomePage)
def add_sidebar_blog_info(request, page):
    sidebar_blog_category = BlogCategory.objects.get(id=1)
    sidebar_blog_posts = BlogPost.objects.all().filter(categories=sidebar_blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    sidebar_blogpost = sidebar_blog_posts.last()
    blogpost_info = BlogPostInfo(sidebar_blogpost)
    return {"sidebar_blogpost": blogpost_info}
