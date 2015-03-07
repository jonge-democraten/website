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


@processor_for(HomePage)
@processor_for(RichTextPage)
def add_header_images(request, page):
    page_header_settings = PageHeaderSettingsWidget.objects.filter(page=page)
    if not page_header_settings:
        return

    page_header_settings = PageHeaderSettingsWidget.objects.get(page=page)

    if page_header_settings.type == PageHeaderSettingsWidget.SINGLE:
        page_header = get_first_page_header(page)
    if page_header_settings.type == PageHeaderSettingsWidget.PARENT:
        parent = page.parent
        if parent:
            page_header = get_parent_page_header(parent)
        else:
            homepage = HomePage.objects.all()[0]
            page_header = get_first_page_header(homepage)
    if page_header_settings.type == PageHeaderSettingsWidget.NONE:
        page_header = None
    if page_header_settings.type == PageHeaderSettingsWidget.RANDOM:
        page_header = get_random_page_header(page)

    if page_header:
        page_header.title = page.title
    return {"page_header": page_header}


@processor_for(HomePage)
def add_column_elements(request, page):
    element_widgets_left = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.LEFT).filter(page=page.homepage)
    column_left_items = create_column_items(element_widgets_left)
    element_widgets_right = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.RIGHT).filter(page=page.homepage)
    column_right_items = create_column_items(element_widgets_right)
    return {"column_left_items": column_left_items, "column_right_items": column_right_items}


def get_first_page_header(page):
    page_header = PageHeaderImageWidget.objects.filter(page=page)
    if page_header.exists():
        return page_header[0]
    else:
        return None


def get_parent_page_header(parent):
    page_header_settings = PageHeaderSettingsWidget.objects.get(page=parent)
    if page_header_settings.type == PageHeaderSettingsWidget.PARENT:
        if parent.parent:
            get_parent_page_header(parent.parent)
        else:
            homepage = HomePage.objects.all()[0]
            return get_first_page_header(homepage)
    elif page_header_settings.type != PageHeaderSettingsWidget.NONE:
        return get_first_page_header(parent)
    else:
        return None


def get_random_page_header(page):
    page_header = PageHeaderImageWidget.objects.filter(page=page)
    if page_header.exists():
        return PageHeaderImageWidget.objects.filter(page=page).order_by('?')[0]
    return None