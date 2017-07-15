import logging
logger = logging.getLogger(__name__)

from website.jdpages.models import HomePage
from website.jdpages.models import PageHeaderImageWidget


def get_page_header(page):
    """
    :returns: the page header for a given page.
    Uses parent page image when none is defined.
    Top parent is the HomePage.
    None when there is no Hompage or when the HomePage has no header.
    """

    # Get a random page header, or the first one if there is only one
    image = PageHeaderImageWidget.objects.filter(page=page).order_by('?').first()
    if image is not None:
        return image

    # No image found! If we received an integer, then do not search further
    if isinstance(page, int):
        return None

    # Try from parent
    if page.parent:
        return get_page_header(page.parent)

    # Try from first homepage
    homepage = HomePage.objects.values_list('id').first()
    if len(homepage) != 0:
        # Since we give get_page_header an integer, there is no infinite recursion here...
        return get_page_header(homepage[0])

    return None


def get_homepage_header():
    """ Returns the page header image of the homepage """
    homepage = HomePage.objects.values_list('id').first()
    if len(homepage) == 0:
        return None
    return get_page_header(homepage[0])
