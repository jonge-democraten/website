from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.models import Displayable, RichText

class Event(Displayable, RichText):
    """
        Main object for each event.

        Derives from Displayable, which by default

        - it is related to a certain Site object
        - it has a title and a slug
        - it has SEO metadata
        - it gets automated timestamps when the object is updated

        Besides that, it derives from RichText, which provides a WYSIWYG field.
    """

class Occurence(models.Model):
    """
        Represents an occurence of an event. Can be automatically repeated
    """

    event = models.ForeignKey(Event)
    start = models.DateTimeField()
    end = models.DateTimeField()

