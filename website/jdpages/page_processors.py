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
from website.jdpages.models import VisionPage
from website.jdpages.models import VisionsPage
from website.jdpages.views import get_page_header


@processor_for(DocumentListing)
@processor_for(Form)
@processor_for(HomePage)
@processor_for(VisionPage)
@processor_for(VisionsPage)
@processor_for(BlogCategoryPage)
@processor_for(RichTextPage)
def add_header_images(request, page):
    page_header = get_page_header(page)

    if page_header:
        page_header.title = page.title
    return {"page_header": page_header}


@processor_for(BlogCategoryPage)
def add_blogposts(request, page):
    template_response = blog_post_list(request, category=page.blogcategorypage.blog_category.slug)
    return {"blog_posts": template_response.context_data["blog_posts"]}
