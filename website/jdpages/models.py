"""
Models that extend mezzanine Pages and add JD specific data.
"""

import logging
logger = logging.getLogger(__name__)

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from mezzanine.blog.models import BlogCategory
from mezzanine.core.models import RichText, Displayable
from mezzanine.pages.models import Page
from mezzanine.utils.sites import Site


class JDContentBase(models.Model):
    """
    Abstract model that provides extra content to a mezzanine page.
    Can be used in new Page mixins. 
    """
    header_image = models.CharField(editable=True, max_length=1000,
                                    blank=True, null=False, default="")

    class Meta:
        abstract = True


class JDColumnItem(models.Model):
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(null=True, verbose_name='related object id')
    content_object = GenericForeignKey('content_type', 'object_id')
    site = models.ForeignKey(Site, default=1, blank=False, null=False)

    def __str__(self):
        return str(self.content_object) + ' (' + str(self.content_type) + ')'
    
    class Meta:
        verbose_name = u'JD Column Item'


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
    column_items_left = models.ManyToManyField(JDColumnItem, blank=True, null=True, related_name="column_items_left")
    column_items_right = models.ManyToManyField(JDColumnItem, blank=True, null=True, related_name="column_items_right")

    class Meta:
        verbose_name = u'JD Homepage'
