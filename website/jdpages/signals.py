import logging
logger = logging.getLogger(__name__)

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.sites.models import Site

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement, EventColumnElement
from website.jdpages.models import Sidebar, SidebarTabsWidget
from website.jdpages.models import create_columnelement_for_blogcategory


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
    if sender == Sidebar:
        logger.info('create sidebar tabs widget...')
        tabs_widget = SidebarTabsWidget.objects.create(sidebar=instance, active=True)
        tabs_widget.site_id = instance.id
        tabs_widget.save(update_site=False)
        logger.info('tabs widget created and saved: ' + str(tabs_widget))

    if sender == BlogCategory:
        if not ColumnElement.objects.filter(object_id=instance.id, content_type=ContentType.objects.get_for_model(sender)):  # TODO BR: move this check to create_columnelement_for_blogcategory function
            logger.info('create blog column element')
            create_columnelement_for_blogcategory(instance, False)
            create_columnelement_for_blogcategory(instance, True)
            logger.info('blog column element created')
    if sender == Site:
        logger.info('create new event column element for site: ' + str(instance.id) + ' (' + str(instance) + ')')
        create_column_element_for_event(EventColumnElement.ALL, instance.id)
        create_column_element_for_event(EventColumnElement.SITE, instance.id)
        if instance.id != 1:  # not the main site
            create_column_element_for_event(EventColumnElement.MAIN_AND_SITE, instance.id)
        logger.info('event column element created')

    return


def create_column_element_for_event(event_type, site_id):
    """ Creates a column element model for a (new) event """
    event_element = EventColumnElement.objects.create(type=event_type)
    event_element.site_id = site_id
    event_element.save(update_site=False)
    element = ColumnElement.objects.create()
    element.name = event_element.get_name()
    element.content_type = ContentType.objects.get_for_model(event_element)
    element.object_id = event_element.id
    element.site_id = site_id
    element.save(update_site=False)


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
        blog_elements = ColumnElement.objects.filter(object_id=instance.id,
                                                     content_type=ContentType.objects.get_for_model(sender))
        related_elements.append(blog_elements)

    for element in related_elements:
        element.delete()

    return
