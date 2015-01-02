from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def post_save_callback(sender, instance, created, **kwargs):
    """
    Called after a model instance is saved.
    """
    
    return # TODO BR: implement