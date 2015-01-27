"""
Models that extend mezzanine Pages and add JD specific data.
"""

from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.core.fields import FileField
from mezzanine.core.models import Orderable, RichText, SiteRelated
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page


class ColumnElement(SiteRelated):
    """
    A generic column element with reference to any model object.
    Designed to be created when a supported model is created, see signals.py.
    The ColumnElementWidget contains the information on how to display the
    model object of this element.
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


class HorizontalPosition():
    """ Horizontal position of a user interface object. """
    LEFT = 'Left'
    RIGHT = 'Right'
    POSITION_CHOICES = (
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    )


class ColumnElementWidget(Orderable, SiteRelated):
    """
    User interface object that shows some data in a html column on a page.
    Contains a reference to some generic data represented by ColumnElement.
    Contains a html item factory that generates the html for the supported
    element types. Each element contains of one or more items.
    """
    title = models.CharField(max_length=1000, blank=True, null=False, default="")
    column_element = models.ForeignKey(ColumnElement, blank=False, null=True)
    page = models.ForeignKey(Page, blank=False, null=True)
    max_items = models.PositiveIntegerField(default=3, blank=False, null=False)
    horizontal_position = models.CharField(max_length=20,
                                           choices=HorizontalPosition.POSITION_CHOICES,
                                           default=HorizontalPosition.RIGHT)

    def __str__(self):
        return str(self.column_element) + ' widget'

    class Meta:
        verbose_name = 'Column widget'


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
    What it shows is determined by its corresponding view item.
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


class SocialMediaButton(Orderable, SiteRelated):
    """ Social media button that can be placed on a sidebar. """

    FACEBOOK = 'FB'
    LINKEDIN = 'LI'
    TWITTER = 'TW'
    YOUTUBE = 'YT'

    SOCIAL_MEDIA_CHOICES = (
        (FACEBOOK, 'Facebook'),
        (LINKEDIN, 'LinkedIn'),
        (TWITTER, 'Twitter'),
        (YOUTUBE, 'YouTube'),
    )

    SOCIAL_MEDIA_ICONS = {
        FACEBOOK: 'facebook.png',
        LINKEDIN: 'linkedin.png',
        TWITTER: 'twitter.png',
        YOUTUBE: 'youtube.png',
    }

    type = models.CharField(max_length=2, choices=SOCIAL_MEDIA_CHOICES)
    url = models.URLField(max_length=200)
    sidebar = models.ForeignKey(Sidebar, blank=False, null=False)

    def get_icon_url(self):
        return 'images/icons/' + SocialMediaButton.SOCIAL_MEDIA_ICONS[str(self.type)]

    def get_type_name(self):
        for choice in SocialMediaButton.SOCIAL_MEDIA_CHOICES:
            if choice[0] == self.type:
                return choice[1]
        assert False  # there should always be a name
        return 'undefined type'

    def __str__(self):
        return str(type)

    class Meta:
        verbose_name = 'Social media button'


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
    description = models.CharField(_("Description"), max_length=1000)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"


def get_public_blogposts(blog_category):
    """ Returns all blogposts for a given category that are published and not expired. """
    blog_posts = BlogPost.objects.all().filter(categories=blog_category).filter(status=CONTENT_STATUS_PUBLISHED)
    return blog_posts.filter(publish_date__lte=datetime.now()).filter(Q(expiry_date__isnull=True)
                                                                      | Q(expiry_date__gte=datetime.now()))


def create_columnelement_for_blogcategory(blog_category):
    blog_category_element = ColumnElement()
    blog_category_element.title = blog_category.title
    blog_category_element.content_type = ContentType.objects.get_for_model(BlogCategory)
    blog_category_element.object_id = blog_category.id
    blog_category_element.save()  # this overrides the site_id, so we set it again below
    blog_category_element.site_id = blog_category.site_id
    blog_category_element.save(update_site=False)
