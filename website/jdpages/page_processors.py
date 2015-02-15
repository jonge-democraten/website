"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from mezzanine.pages.page_processors import processor_for
from mezzanine.pages.models import RichTextPage

from website.jdpages.models import HomePage, ColumnElementWidget
from website.jdpages.models import HorizontalPosition
from website.jdpages.models import PageHeaderSettingsWidget, PageHeaderImageWidget
from website.jdpages.views import create_column_items

@processor_for(RichTextPage)
def add_header_images(request, page):
    page_header_settings = PageHeaderSettingsWidget.objects.get(page=page)
    page_header = []
    if page_header_settings.type == PageHeaderSettingsWidget.SINGLE:
        page_header = PageHeaderImageWidget.objects.filter(page=page)[0]
    if page_header_settings.type == PageHeaderSettingsWidget.PARENT:
        parent = page.parent
        if parent:
            page_header = PageHeaderImageWidget.objects.filter(page=parent)[0]
        else:
            homepage = HomePage.objects.all()[0]
            page_header = PageHeaderImageWidget.objects.filter(page=homepage)[0]
    if page_header_settings.type == PageHeaderSettingsWidget.NONE:
        page_header = []
    if page_header_settings.type == PageHeaderSettingsWidget.RANDOM:
        page_headers = PageHeaderImageWidget.objects.filter(page=page)
        page_headers
    return {"page_header": page_header}


@processor_for(HomePage)
def add_column_elements(request, page):
    element_widgets_left = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.LEFT).filter(page=page.homepage)
    column_left_items = create_column_items(element_widgets_left)
    element_widgets_right = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.RIGHT).filter(page=page.homepage)
    column_right_items = create_column_items(element_widgets_right)
    return {"column_left_items": column_left_items, "column_right_items": column_right_items}
