"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from django.conf import settings


from mezzanine.blog.models import BlogCategory, BlogPost
from mezzanine.pages.page_processors import processor_for

from website.jdpages.models import JDPage, JDHomePage, JDColumnElement, BlogCategoryElement
from website.utils.containers import BlogPostItem


@processor_for(JDHomePage)
def add_column_elements(request, page):
    elements_left = page.jdhomepage.column_elements_left.all()
    elements_org_left = get_original_elements(elements_left)
    elements_right= page.jdhomepage.column_elements_right.all()
    elements_org_right = get_original_elements(elements_right)
    return {"column_elements_left": elements_org_left,
            "column_elements_right": elements_org_right}


def get_original_elements(elements):
    elements_new = []
    for element in elements:
        if element.content_type.model_class() == BlogCategory:
            elements_new.append(BlogCategoryElement.get_blog_category_element(element))
    return elements_new
