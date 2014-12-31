"""
Models that extend mezzanine Pages and add JD specific data.
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models

from mezzanine.core.models import RichText
from mezzanine.pages.models import Page


class JDContentBase(models.Model):
    """
    Abstract model that provides extra content to a mezzanine page.
    Can be used in new Page mixins. 
    """
    header_image = models.CharField(editable=True, max_length=1000,
                                    blank=True, null=False, default="")

    class Meta:
        abstract = True


class JDPage(Page, RichText, JDContentBase):
    """
    Page model for general richtext pages
    """


class JDHomePage(Page, RichText, JDContentBase):
    """
    Page model for the JD homepage (jd.nl)
    """
