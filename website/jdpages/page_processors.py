"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.pages.page_processors import processor_for

from website.jdpages.models import JDHomePage
from website.utils.containers import HorizontalPosition
from website.jdpages.views import get_elements_with_items


@processor_for(JDHomePage)
def add_column_elements(request, page):
    elements_left = page.jdhomepage.get_column_elements(HorizontalPosition.LEFT)
    elements_left = get_elements_with_items(elements_left)
    elements_right =  page.jdhomepage.get_column_elements(HorizontalPosition.RIGHT)
    elements_right = get_elements_with_items(elements_right)
    return { "column_elements_left": elements_left, "column_elements_right": elements_right }
