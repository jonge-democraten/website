"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.pages.page_processors import processor_for

from website.jdpages.models import HomePage, ColumnElement
from website.utils.containers import HorizontalPosition


@processor_for(HomePage)
def add_column_elements(request, page):
    logger.warning('TEST')
    elements_left = page.homepage.get_column_elements(HorizontalPosition.LEFT)
    elements_left = ColumnElement.get_elements_with_items(elements_left)
    elements_right =  page.homepage.get_column_elements(HorizontalPosition.RIGHT)
    elements_right = ColumnElement.get_elements_with_items(elements_right)
    return { "column_elements_left": elements_left, "column_elements_right": elements_right }
