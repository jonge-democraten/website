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

    page_header = get_page_header(page)

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


def get_page_header(page):
    page_header_settings = PageHeaderSettingsWidget.objects.get(page=page)

    if page_header_settings.type == PageHeaderSettingsWidget.SINGLE:
        return get_first_page_header(page)
    elif page_header_settings.type == PageHeaderSettingsWidget.PARENT:
        if page.parent:
            return get_page_header(page.parent)
        else:
            homepages = HomePage.objects.all()
            if homepages.exists():
                return get_page_header(homepages[0])
            else:
                return None
    elif page_header_settings.type == PageHeaderSettingsWidget.NONE:
        return None
    elif page_header_settings.type == PageHeaderSettingsWidget.RANDOM:
        return get_random_page_header(page)


def get_random_page_header(page):
    page_header = PageHeaderImageWidget.objects.filter(page=page)
    if page_header.exists():
        return PageHeaderImageWidget.objects.filter(page=page).order_by('?')[0]
    return None