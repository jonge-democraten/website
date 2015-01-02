"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)
from datetime import datetime

from django.conf import settings
from django.db.models import Q

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.page_processors import processor_for

from .models import JDPage, JDHomePage
from website.utils.containers import BlogPostInfo


@processor_for(JDHomePage)
def add_left_column_blogposts(request, page):
    blog_posts = get_public_blogposts(settings.HOMEPAGE_LEFT_COLUMN_BLOG)[:3]
    blogposts_info = []
    for post in blog_posts:
        blogposts_info.append(BlogPostInfo(post))
    return {"leftcolumn_blogposts_info": blogposts_info}


@processor_for(JDHomePage)
def add_right_column_blogposts(request, page):
    blog_posts = get_public_blogposts(settings.HOMEPAGE_RIGHT_COLUMN_BLOG)[:3]
    blogposts_info = []
    for post in blog_posts:
        blogposts_info.append(BlogPostInfo(post))
    return {"rightcolumn_blogposts_info": blogposts_info}


def get_public_blogposts(blogcategory):
    try: 
        blog_category = BlogCategory.objects.get(title=blogcategory)
    except BlogCategory.DoesNotExist:
        return [] # the blog category may not exist
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=datetime.now()).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=datetime.now()))
