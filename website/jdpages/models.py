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
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.fields import FileField
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
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=False, null=True, verbose_name='related object id')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.content_object) + ' (' + str(self.content_type) + ')'

    def get_object(self):
        """ Returns the content object. """
        return self.content_type.model_class().objects.get(id=self.object_id)

    class Meta:
        verbose_name = 'Column element'


class ColumnElementWidget(Orderable, SiteRelated):
    """ """
    title = models.CharField(max_length=1000, blank=True, null=False, default="")
    column_element = models.ForeignKey(ColumnElement, blank=False, null=True)
    page = models.ForeignKey(Page, blank=False, null=True)
    max_items = models.PositiveIntegerField(default=3, blank=False, null=False)
    horizontal_position = models.CharField(max_length=20, 
                                           choices=HorizontalPosition.POSITION_CHOICES, 
                                           default=HorizontalPosition.RIGHT)

    @staticmethod
    def add_items_to_widgets(element_widgets):
        """ 
        Adds the items to this element 
        Contains a ContentType type switch which determines 
        element_widgets --- a list of ColumnElements
        """
        for widget in element_widgets:
            if widget.column_element.content_type.model_class() == BlogCategory:
                widget.items = []
                blogposts = get_public_blogposts(widget.column_element.get_object())[:widget.max_items]
                for post in blogposts:
                    widget.items.append(BlogPostItem(post))
        return element_widgets

    def __str__(self):
        return str(self.column_element) + ' widget'

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

    class Meta:
        verbose_name = 'Homepage'


class DocumentListing(Page, RichText, ContentBase):
    """
    Page model for document listing pages.
    """
    class Meta:
        verbose_name = "Document Listing"
        verbose_name_plural = "Document Listings"


class Document(Orderable):
    """
    Model for a document in a DocumentListing.
    """

    document_listing = models.ForeignKey(DocumentListing, related_name="documents")
    document = FileField(_("Document"), max_length = 200, format = "Document")
    description = models.CharField(_("Description"), max_length = 1000)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


def get_public_blogposts(blog_category):
    """ Returns all blogposts for a given category that are published and not expired. """
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=datetime.now()).filter(Q(expiry_date__isnull=True) | Q(expiry_date__gte=datetime.now()))
