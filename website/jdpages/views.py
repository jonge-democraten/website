import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import get_public_blogposts


def create_column_items(column_widgets):
    column_items = []
    for widget in column_widgets:
        model_class = widget.column_element.content_type.model_class()
        if model_class == BlogCategory:
            blog_category = widget.column_element.get_object()
            column_items.append(BlogCategoryItem(blog_category, widget.max_items))
    return column_items


class ColumnItem(object):
    def get_template_name(self):
        return "none"


class BlogCategoryItem(ColumnItem):
    def __init__(self, blogcategory, max_posts):
        self.title = blogcategory.title
        self.children = self.create_children(blogcategory, max_posts)

    @staticmethod
    def create_children(blogcategory, max_items):
        children = []
        blogposts = get_public_blogposts(blogcategory)[:max_items]
        for post in blogposts:
            children.append(BlogPostItem(post))
        return children

    def get_template_name(self):
        return "blogcategory_column_item.html"


class BlogPostItem(object):
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)
