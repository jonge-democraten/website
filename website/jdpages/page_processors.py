"""
Mezzanine page processors for jdpages.
Read the mezzanine documentation for more info.
"""

import logging

from mezzanine.blog.views import blog_post_list
from mezzanine.pages.page_processors import processor_for
from mezzanine.pages.models import RichTextPage

from website.jdpages.models import BlogCategoryPage
from mezzanine.forms.models import Form
from website.jdpages.models import HomePage
from website.jdpages.models import OrganisationPage
from website.jdpages.models import OrganisationPartPage
from website.jdpages.models import VisionPage
from website.jdpages.models import VisionsPage
from website.jdpages.models import WordLidPage
from website.jdpages.views import get_page_header

logger = logging.getLogger(__name__)

@processor_for(Form)
@processor_for(HomePage)
@processor_for(VisionPage)
@processor_for(VisionsPage)
@processor_for(OrganisationPage)
@processor_for(OrganisationPartPage)
@processor_for(BlogCategoryPage)
@processor_for(RichTextPage)
@processor_for(WordLidPage)
def add_header_images(request, page):
    page_header = get_page_header(page)

    if page_header:
        page_header.title = page.title
    return {"page_header": page_header}


@processor_for(BlogCategoryPage)
def add_blogposts(request, page):
    template_response = blog_post_list(request, category=page.blogcategorypage.blog_category.slug)
    return {"blog_posts": template_response.context_data["blog_posts"]}
