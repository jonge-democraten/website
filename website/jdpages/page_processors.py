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
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)


@processor_for(JDPage)
@processor_for(JDHomePage)
def add_sidebar_blog_info(request, page):
    sidebar_blog_category = BlogCategory.objects.get(id=1)
    sidebar_blog_posts = BlogPost.objects.all().filter(categories=sidebar_blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    sidebar_blogpost = sidebar_blog_posts.last()
    if not sidebar_blogpost:
        return
    blogpost_info = BlogPostInfo(sidebar_blogpost)
    return {"sidebar_blogpost": blogpost_info}


@processor_for(JDHomePage)
def add_politiek_blogposts(request, page):
    politiek_blog_category = BlogCategory.objects.get(title="Politiek")
    politiek_blog_posts = BlogPost.objects.all().filter(categories=politiek_blog_category).filter(status=CONTENT_STATUS_PUBLISHED)[:3]
    politiek_blogposts_info = []
    for post in politiek_blog_posts:
        politiek_blogposts_info.append(BlogPostInfo(post))
    return {"politiek_blogposts_info": politiek_blogposts_info}
