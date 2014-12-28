import logging
logger = logging.getLogger(__name__)

from django.db import models

from mezzanine.core.models import RichText
from mezzanine.pages.models import Page


class JDContentBase(models.Model):
    """
    """
    header_image = models.CharField(editable=True, max_length=1000, 
                                    blank=True, null=False, default="")

    class Meta:
        abstract = True


class JDPage(Page, RichText, JDContentBase):
    """
    """