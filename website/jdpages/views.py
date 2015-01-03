import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import BlogCategoryElement

def get_elements_with_items(elements):
    """ 
    Adds the element items to this element 
    Contains a ContentType type switch which determines 
    elements --- a list of ColumnElementWidgets
    """
    elements_new = []
    for element in elements:
        if element.content_type.model_class() == BlogCategory:
            elements_new.append(BlogCategoryElement.get_element_with_items(element))
    return elements_new
