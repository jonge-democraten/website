"""
Models that extend mezzanine Pages and add JD specific data.
"""

from datetime import datetime
import os
from string import punctuation
import logging
logger = logging.getLogger(__name__)

from PIL import Image

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils import timezone
from django.conf import settings

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText, SiteRelated
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page


def validate_header_image(imagepath):
    """ Validates the resolution of a header image. """
    absolute_imagepath = os.path.join(settings.MEDIA_ROOT, str(imagepath))
    im = Image.open(absolute_imagepath)
    width, height = im.size
    if width != 610 or height != 290:
        raise ValidationError('Image should be 610 x 290 pixels, selected image is %i x %i. Please resize the image.' % (width, height))


class PageHeaderImageWidget(SiteRelated):
    """ Page header image. """
    name = models.CharField(max_length=1000, blank=True, null=False, default="")
    page = models.ForeignKey(Page, blank=False, null=True)
    image = FileField(max_length=200, format="Image", validators=[validate_header_image])


class Sidebar(SiteRelated):
    """ Site sidebar that can contain sidebar widgets. """

    def __str__(self):
        return "Sidebar"

    class Meta:
        verbose_name = "Sidebar"
        verbose_name_plural = "Sidebar"


class SidebarBlogCategoryWidget(SiteRelated):
    """
    Blog category widget that can be placed on a sidebar.
    Its corresponding view item contains the template information.
    """
    title = models.CharField(max_length=200, blank=False, null=False, default="")
    sidebar = models.ForeignKey(Sidebar, blank=False, null=False)
    blog_category = models.ForeignKey(BlogCategory, blank=False, null=True)

    def __str__(self):
        return str(self.blog_category) + ' widget'

    class Meta:
        verbose_name = 'Sidebar blogcategory'


class SidebarTwitterWidget(SiteRelated):
    """
    Twitter widget that can be placed on a sidebar.
    The actual twitter settings can be found in the site settings.
    This is just the element that can be placed on a sidebar.
    """
    active = models.BooleanField(default=False, blank=False, null=False)
    sidebar = models.OneToOneField(Sidebar, blank=False, null=False)

    class Meta:
        verbose_name = 'Sidebar twitter widget'


class SidebarBannerWidget(models.Model):
    """ Banner that can be placed on a sidebar """
    title = models.CharField(max_length=200, blank=False, null=False, default="")
    active = models.BooleanField(blank=False, null=False, default=True)
    image = FileField(max_length=200, format="Image")
    url = models.URLField(max_length=200, help_text='http://www.example.com')
    description = models.CharField(max_length=200, blank=True, null=False, default="",
                                   help_text='This is shown as tooltip and alt text.')

    def __str__(self):
        return str(self.title) + ' widget'

    class Meta:
        verbose_name = 'Global sidebar banner'


class HomePage(Page, RichText):
    """
    Page model for the site homepage.
    Only works properly when url points to the homepage '/' as url.
    """

    class Meta:
        verbose_name = 'Homepage'


class DocumentListing(Page, RichText):
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
    document = FileField(_("Document"), max_length=200, format="Document")
    description = models.CharField(_("Description"), max_length=1000, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def save(self, *args, **kwargs):
        """
        If no description is given when created, create one from the
        file name.

        Code copied from mezzanine.galleries.models.GalleryImage
        """
        if not self.description:
            name = force_text(self.document.name)
            name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
            name = name.replace("'", "")
            name = "".join([c if c not in punctuation else " " for c in name])
            name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
                            for i, s in enumerate(name)])
            self.description = name
        super(Document, self).save(*args, **kwargs)


class EventColumnElement(SiteRelated):
    """ Column Element model for an Event """
    SITE = 'SI'
    ALL = 'AL'
    MAIN = 'MA'
    MAIN_AND_SITE = 'SM'

    EVENT_CHOICES = (
        (SITE, 'Site'),
        (ALL, 'All'),
        (MAIN, 'Main site'),
        (MAIN_AND_SITE, 'Main and site'),
    )

    type = models.CharField(max_length=2, choices=EVENT_CHOICES)

    def get_name(self):
        if self.type == self.MAIN_AND_SITE:
            return 'Events for current and main site'
        elif self.type == self.ALL:
            return 'Events for all sites'
        elif self.type == self.SITE:
            return 'Events for current site'
        elif self.type == self.MAIN:
            return 'Events for main site'
        assert False

    def __str__(self):
        return self.get_name()


class BlogCategoryPage(Page, RichText):
    """
    Model for a page that displays a list of posts in a single blog category.
    """

    blog_category = models.ForeignKey(BlogCategory, null=False, blank=False)
    show_excerpt = models.BooleanField(default=False, null=False, blank=False,
                                       help_text='Show only the first paragraph of a blog post.')

    class Meta:
        verbose_name = "Blog category page"
        verbose_name_plural = "Blog category pages"


def get_public_blogposts(blog_category):
    """ Returns all blogposts for a given category that are published and not expired. """
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=timezone.now()).filter(Q(expiry_date__isnull=True)
                                                                      | Q(expiry_date__gte=timezone.now()))
