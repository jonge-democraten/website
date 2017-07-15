import logging
logger = logging.getLogger(__name__)

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.sites.models import Site

from website.jdpages.models import Sidebar


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
    if not created:
        return

    if sender == Site:
        logger.info('create new sidebar for site: ' + str(instance.id) + ' (' + str(instance) + ')')
        main_sidebar = Sidebar.objects.create()
        main_sidebar.site_id = instance.id
        main_sidebar.save(update_site=False)
        logger.info('sidebar created and saved')
    return
