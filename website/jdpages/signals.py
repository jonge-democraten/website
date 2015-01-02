from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import JDColumnItem


@receiver(post_save)
def post_save_callback(sender, instance, created, **kwargs):
    """
    Called after a model instance is saved.
    Created related database objects for some 
    
    Arguments:
    sender -- the model class
    instance -- the actual instance being saved
    created -- a boolean; True if a new record was created
    """
    if not created:
        return
    if (sender == BlogCategory):
        if JDColumnItem.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender)):
            return
        column_item = JDColumnItem()
        column_item.content_type = ContentType.objects.get_for_model(sender)
        column_item.object_id = instance.id
        column_item.site = instance.site
        column_item.save()
        return
