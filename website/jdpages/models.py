"""
Models that extend mezzanine Pages and add JD specific data.
"""

import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField
from mezzanine.core.models import RichText, Orderable
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


class DocumentListing(Page, RichText, JDContentBase):
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

    document_listing = models.ForeignKey("DocumentListing", related_name="documents")
    document = FileField(_("Document"), max_length = 200, format = "Document")
    description = models.CharField(_("Description"), max_length = 1000)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
