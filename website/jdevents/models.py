from django.db import models

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

    event_date = models.DateTimeField()
    event_end = models.DateTimeField()

