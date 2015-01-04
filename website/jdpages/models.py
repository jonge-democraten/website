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
from mezzanine.core.models import Orderable, RichText, Displayable, SiteRelated
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page
from mezzanine.utils.sites import Site

from website.utils.containers import BlogPostItem, HorizontalPosition
     

class ColumnElement(SiteRelated):
    """ 
    Generic graphical column element.
    Contains a reference to a generic ContentType derived object.
    The referenced object is responsible for adding items to this element.
    Designed to be created on creation of such objects.
    """
    title = models.CharField(max_length=1000, blank=True, null=False, default="")
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=False, null=True, verbose_name='related object id')
    content_object = GenericForeignKey('content_type', 'object_id')
    max_items = models.PositiveIntegerField(default=3, blank=False, null=False)

    def __str__(self):
        return str(self.content_object) + ' (' + str(self.content_type) + ')'

    def get_object(self):
        """ Returns the content object. """
        return self.content_type.model_class().objects.get(id=self.object_id)
    
    @staticmethod
    def get_elements_with_items(elements):
        """ 
        Adds the items to this element 
        Contains a ContentType type switch which determines 
        elements --- a list of ColumnElements
        """
        for element in elements:
            if element.content_type.model_class() == BlogCategory:
                element.items = []
                blogposts = get_public_blogposts(element.get_object())[:element.max_items]
                for post in blogposts:
                    element.items.append(BlogPostItem(post))
        return elements

    class Meta:
        verbose_name = 'Column element'


class ColumnElementWidget(Orderable, SiteRelated):
    """ """
    column_element = models.ForeignKey(ColumnElement, blank=False, null=True)
    page = models.ForeignKey(Page, blank=False, null=True)
    horizontal_position = models.CharField(max_length=20, 
                                           choices=HorizontalPosition.POSITION_CHOICES, 
                                           default=HorizontalPosition.RIGHT)
    
    def __str__(self):
        return str(self.column_element) + ' widget'
    
    @staticmethod
    def get_widgets(horizontal_position):
        return ColumnElementWidget.objects.filter(horizontal_position=horizontal_position)

    class Meta:
        verbose_name = 'Column element widget'


class ContentBase(models.Model):
    """
    Abstract model that provides extra content to a mezzanine page.
    Can be used in new Page mixins. 
    """
    header_image = models.CharField(editable=True, max_length=1000,
                                    blank=True, null=False, default="")

    class Meta:
        abstract = True


class JDPage(Page, RichText, ContentBase):
    """ Page model for general richtext pages. """

    class Meta:
        verbose_name = 'JD Page'


class HomePage(Page, RichText, ContentBase):
    """ Page model for the site homepage. """

    def get_column_elements(self, hor_pos):
        element_widgets = ColumnElementWidget.get_widgets(hor_pos).filter(page=self)
        elements = []
        for widget in element_widgets:
            elements.append(widget.column_element)
        return elements

    class Meta:
        verbose_name = 'Homepage'

        

def get_public_blogposts(blog_category):
    """ Returns all blogposts for a given category that are published and not expired. """
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=datetime.now()).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=datetime.now()))
