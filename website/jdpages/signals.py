import logging
logger = logging.getLogger(__name__)

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement
from website.jdpages.models import SocialMediaButtonGroup 
from website.jdpages.models import SidebarElement
from website.jdpages.models import create_columnelement_for_blogcategory
from website.jdpages.models import create_sidebarelement_for_socialmediagroup


@receiver(post_save)
def post_save_callback(sender, instance, created, **kwargs):
    """
    Called after a model instance is saved.
    Create related models here.
    Arguments:
    sender -- the model class
    instance -- the actual instance being saved
    created -- a boolean; True if a new record was created
    """
    logger.warning('post_save')
    if not created:
        return
    if sender == BlogCategory:
        if ColumnElement.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender)):
            return
        create_columnelement_for_blogcategory(instance)
    elif sender == SocialMediaButtonGroup:
        if SidebarElement.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender)):
            return
        create_sidebarelement_for_socialmediagroup(instance)
    return


@receiver(pre_delete)
def pre_delete_callback(sender, instance, **kwargs):
    """
    Called just before a model is deleted.
    Delete related models here. 
    Arguments:
    sender -- the model class
    instance -- the actual instance being saved
    """
    related_elements = []
    if sender == BlogCategory:
        related_elements = ColumnElement.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender))
    elif sender == SocialMediaButtonGroup:
        related_elements = SidebarElement.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender))
    for element in related_elements:
        element.delete()    
    return
