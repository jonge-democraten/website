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
from mezzanine.core.fields import RichTextField
from mezzanine.core.models import Orderable, RichText, SiteRelated
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED
from mezzanine.pages.models import Page


class FooterLinks(SiteRelated):
    title = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.title


class FooterLink(SiteRelated, Orderable):
    title = models.CharField(max_length=100, blank=True, default="")
    url = models.CharField(max_length=500, blank=True, default="")
    footer_links = models.ForeignKey(FooterLinks, blank=True, null=True)

    def __str__(self):
        return self.title


class FooterInfo(SiteRelated):
    title = models.CharField(max_length=100, blank=True, default="")
    content = RichTextField()

    def __str__(self):
        return self.title


class Footer(SiteRelated):
    links_left = models.OneToOneField(FooterLinks, auto_created=True, related_name="links_left")
    links_middle = models.OneToOneField(FooterLinks, auto_created=True, related_name="links_right")
    info_right = models.OneToOneField(FooterInfo, auto_created=True)

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"


def validate_header_image(imagepath):
    """ Validates the resolution of a header image. """
    absolute_imagepath = os.path.join(settings.MEDIA_ROOT, str(imagepath))
    if not os.path.exists(absolute_imagepath):
        raise ValidationError('The file for this header does not exist anymore. Please remove or replace this header before saving the page.')
    im = Image.open(absolute_imagepath)
    width, height = im.size
    aspect_ratio = width/height
    if aspect_ratio < 2.0:
        raise ValidationError('Image aspect ratio should be at least 2 (for example 2000x1000px). The selected image is %i x %i. Please resize the image.' % (width, height))
    if width < 1000:
        raise ValidationError('Image resolution is too low. It should be at least 1000px wide. The selected image is %i x %i. Please find a larger image.' % (width, height))


class PageHeaderImage(SiteRelated):
    """ Page header image. """
    name = models.CharField(max_length=1000, blank=True, null=False, default="")
    page = models.ForeignKey(Page, blank=False, null=True)
    image = FileField(max_length=200, format="Image", validators=[validate_header_image])


class PageItem(SiteRelated):
    page = models.ForeignKey(Page, blank=False, null=True)
    visible = models.BooleanField(default=True)

    class Meta:
        abstract = True


class SidebarAgenda(PageItem):
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

    class Meta:
        verbose_name = "Sidebar Agenda Item"

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


class SidebarTwitter(PageItem):

    class Meta:
        verbose_name = "Sidebar Twitter Item"


class SidebarSocial(PageItem):

    @property
    def urls(self):
        smulrs = SocialMediaUrls.objects.all()
        if smulrs.exists():
            return smulrs[0]
        return None

    class Meta:
        verbose_name = "Sidebar Social Media Item"


class SidebarRichText(PageItem):
    title = models.CharField(max_length=100, blank=True, default="")
    content = RichTextField()

    class Meta:
        verbose_name = "Sidebar RichText Item"

    def __str__(self):
        return self.title


class SidebarLink(PageItem, Orderable):
    title = models.CharField(max_length=100, blank=True, default="")
    url = models.CharField(max_length=500, blank=True, default="")


class ActionBanner(PageItem):
    title = models.CharField(max_length=500, blank=True, default="")
    content = RichTextField()
    image = FileField(max_length=300, format="Image")
    button_title = models.CharField(max_length=500, blank=True, default="")
    button_url = models.CharField(max_length=500, blank=True, default="")

    def __str__(self):
        return self.title


def validate_images_aspect_ratio(imagepath, required_aspect_ratio, max_difference):
    """ Validates the aspect ratio of an image. """
    absolute_imagepath = os.path.join(settings.MEDIA_ROOT, str(imagepath))
    im = Image.open(absolute_imagepath)
    width, height = im.size
    aspect_ratio = width/height
    if abs(aspect_ratio - required_aspect_ratio) > max_difference:
        raise ValidationError('Image aspect ratio should be %i, selected image is %i x %i. Please resize the image.' % (required_aspect_ratio, width, height))


def validate_vision_image(imagepath, aspect_ratio, max_difference):
    validate_images_aspect_ratio(imagepath, required_aspect_ratio=1.5, max_difference=0.1)


class VisionPage(Page, RichText):
    """
    """
    image = FileField(max_length=300, format="Image", blank=True, default="", validators=[validate_vision_image])

    class Meta:
        verbose_name = 'Standpunt pagina'
        verbose_name_plural = "Standpunt paginas"


class VisionsPage(Page, RichText):
    """
    """
    vision_pages = models.ManyToManyField(VisionPage, blank=True)

    class Meta:
        verbose_name = 'Standpunten pagina'
        verbose_name_plural = "Standpunten paginas"


def validate_organisation_image(imagepath):
    validate_images_aspect_ratio(imagepath, required_aspect_ratio=1.5, max_difference=0.1)


class OrganisationPartPage(Page, RichText):
    """
    """
    image = FileField(max_length=300, format="Image", blank=True, default="", validators=[validate_organisation_image])

    class Meta:
        verbose_name = 'Organisatie-onderdeel pagina'
        verbose_name_plural = "Organisatie-onderdeel paginas"


class OrganisationPage(Page, RichText):
    """
    """
    organisation_part_pages = models.ManyToManyField(OrganisationPartPage, blank=True)

    class Meta:
        verbose_name = 'Organisatie pagina'
        verbose_name_plural = "Organisatie paginas"


class OrganisationMember(SiteRelated):
    """
    """
    name = models.CharField(max_length=200, blank=False, default="")
    content = RichTextField()
    image = FileField(max_length=300, format="Image", blank=True, default="")
    facebook_url = models.URLField(blank=True, default="")
    twitter_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = 'Organisatie lid'
        verbose_name_plural = "Organisatie leden"

    def __str__(self):
        return self.name


class OrganisationPartMember(SiteRelated):
    member = models.ForeignKey(OrganisationMember)
    organisation_part = models.ForeignKey(OrganisationPartPage, null=True, blank=True)
    role = models.CharField(max_length=200, blank=False, default="")

    class Meta:
        verbose_name = 'Organisatie functie'
        verbose_name_plural = "Organisatie functies"

    def __str__(self):
        return self.role + ' - ' + self.member.name


class HomePage(Page, RichText):
    """
    Page model for the site homepage.
    Only works properly when url points to the homepage '/' as url.
    """
    header_title = models.CharField(max_length=300, blank=True, default="")
    header_subtitle = models.CharField(max_length=500, blank=True, default="")
    news_category = models.ForeignKey(BlogCategory, null=True, blank=True)
    vision_pages = models.ManyToManyField(VisionPage, blank=True, verbose_name="Standpunt paginas")

    @property
    def blog_posts(self):
        return get_public_blogposts(self.news_category)

    class Meta:
        verbose_name = 'Homepage'


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


class SocialMediaUrls(SiteRelated):
    facebook_url = models.URLField(max_length=300, blank=True, default="")
    twitter_url = models.URLField(max_length=300, blank=True, default="")
    youtube_url = models.URLField(max_length=300, blank=True, default="")
    linkedin_url = models.URLField(max_length=300, blank=True, default="")
    instagram_url = models.URLField(max_length=300, blank=True, default="")

    class Meta:
        verbose_name = "Social media urls"
        verbose_name_plural = "Social media urls"
