from django.db import models

class Event(models.Model):
    """
        Main object for each event
    """

    title = models.CharField(max_length=200)

