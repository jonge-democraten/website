"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging
logger = logging.getLogger(__name__)

from mezzanine.blog.views import blog_post_list
from mezzanine.pages.page_processors import processor_for
from mezzanine.pages.models import RichTextPage

from website.jdpages.models import BlogCategoryPage
from mezzanine.forms.models import Form
from website.jdpages.models import HomePage, DocumentListing
from website.jdpages.models import ColumnElementWidget
from website.jdpages.models import HorizontalPosition
from website.jdpages.views import create_column_items, get_page_header


@processor_for(DocumentListing)
@processor_for(Form)
@processor_for(HomePage)
@processor_for(BlogCategoryPage)
@processor_for(RichTextPage)
def add_header_images(request, page):
    page_header = get_page_header(page)

    if page_header:
        page_header.title = page.title
    return {"page_header": page_header}


@processor_for(HomePage)
@processor_for(RichTextPage)
def add_column_elements(request, page):
    element_widgets_left = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.LEFT).filter(page=page)
    column_left_items = create_column_items(element_widgets_left)
    element_widgets_right = ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.RIGHT).filter(page=page)
    column_right_items = create_column_items(element_widgets_right)
    return {"column_left_items": column_left_items, "column_right_items": column_right_items}


@processor_for(BlogCategoryPage)
def add_blogposts(request, page):
    template_response = blog_post_list(request, category=page.blogcategorypage.blog_category.slug)
    return {"blog_posts": template_response.context_data["blog_posts"]}
