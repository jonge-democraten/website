from django.db import models

from mezzanine.core.models import Displayable, RichText


class RepeatType(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly',
    MONTHLY = 'monthly'

    REPEAT_CHOICES = (
        (DAILY, 'REPEAT_DAILY'),
        (WEEKLY, 'REPEAT_WEEKLY'),
        (MONTHLY, 'REPEAT_MONTHLY')
    )

    repeat_type = models.CharField(max_length=10, choices=REPEAT_CHOICES)

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
    repeat = models.ForeignKey(RepeatType, default=None, blank=True)

