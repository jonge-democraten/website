"""
Models that extend mezzanine Pages and add JD specific data.
"""

import logging
logger = logging.getLogger(__name__)
from datetime import datetime


from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.models import RichText, Displayable
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page
from mezzanine.utils.sites import Site

from website.utils.containers import BlogPostItem


class JDContentBase(models.Model):
    """
    Abstract model that provides extra content to a mezzanine page.
    Can be used in new Page mixins. 
    """
    header_image = models.CharField(editable=True, max_length=1000,
                                    blank=True, null=False, default="")

    class Meta:
        abstract = True


class JDColumnElement(models.Model):
    title = models.CharField(editable=True, max_length=1000,
                             blank=True, null=False, default="")
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(null=True, verbose_name='related object id')
    content_object = GenericForeignKey('content_type', 'object_id')
    site = models.ForeignKey(Site, default=1, blank=False, null=False)
    max_items = models.PositiveIntegerField(default=3, blank=False, null=False)

    def __str__(self):
        return str(self.content_object) + ' (' + str(self.content_type) + ')'

    def get_object(self):
        return self.content_type.model_class().objects.get(id=self.object_id)

    class Meta:
        verbose_name = u'Column element'


class BlogCategoryElement(JDColumnElement):         
    @staticmethod
    def get_blog_category_element(element):
        blog_cat_element = BlogCategoryElement.objects.get(id=element.id)
        blog_cat_element.items = []
        blogposts = get_public_blogposts(element.get_object())[:element.max_items]
        for post in blogposts:
            blog_cat_element.items.append(BlogPostItem(post))
        return blog_cat_element


class JDPage(Page, RichText, JDContentBase):
    """
    Page model for general richtext pages.
    """

    class Meta:
        verbose_name = u'JD Page'


class JDHomePage(Page, RichText, JDContentBase):
    """
    Page model for the site homepage
    """
    column_elements_left = models.ManyToManyField(JDColumnElement, blank=True, null=True, related_name="column_elements_left")
    column_elements_right = models.ManyToManyField(JDColumnElement, blank=True, null=True, related_name="column_elements_right")

    class Meta:
        verbose_name = u'JD Homepage'


def get_public_blogposts(blog_category):
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=datetime.now()).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=datetime.now()))
