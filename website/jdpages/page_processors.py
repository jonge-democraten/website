"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings

from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.pages.page_processors import processor_for

from website.jdpages.models import JDPage, JDHomePage, ColumnElementWidget, BlogCategoryElement
from website.utils.containers import BlogPostItem
from website.jdpages.views import get_elements_with_items


@processor_for(JDHomePage)
def add_column_elements(request, page):
    elements_left = page.jdhomepage.column_elements_left.all()
    elements_org_left = get_elements_with_items(elements_left)
    elements_right= page.jdhomepage.column_elements_right.all()
    elements_org_right = get_elements_with_items(elements_right)
    return {"column_elements_left": elements_org_left,
            "column_elements_right": elements_org_right}
