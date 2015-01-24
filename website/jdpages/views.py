import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory, BlogPost

from website.jdpages.models import get_public_blogposts
from website.jdpages.models import SocialMediaButtonGroup


def create_sidebar_items(sidebar_widgets):
    items = []
    for widget in sidebar_widgets:
        model_type = widget.sidebar_element.content_type.model_class()
        if model_type == SocialMediaButtonGroup:
            button_group = widget.sidebar_element.get_object()
            item = SocialMediaButtonGroupItem(button_group)
            item.title = widget.title
            items.append(item)
        elif model_type == BlogCategory:
            blogcategory = widget.sidebar_element.get_object()
            item = BlogCategorySidebarItem(blogcategory)
            item.title = widget.title
            items.append(item)

    return items


class Item(object):
    def get_template_name(self):
        return "none"


class BlogPostItem(Item):
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)

    def get_template_name(self):
        return "blogpostitem.html"


class BlogCategorySidebarItem(Item):
    def __init__(self, blogcategory):
        logger.warning(blogcategory.title)
        self.children = self.create_children(blogcategory)

    @staticmethod
    def create_children(blogcategory):
        children = []
        blogposts = get_public_blogposts(blogcategory)
        for post in blogposts:
            children.append(BlogPostItem(post))
        return children

    def get_template_name(self):
        return "blogpost_sidebar_item.html"


class SocialMediaButtonGroupItem(Item):
    def __init__(self, group):
        from website.jdpages.models import SocialMediaButton
        buttons = SocialMediaButton.objects.filter(social_media_group=group)
        self.children = []
        for button in buttons:
            self.children.append(SocialMediaButtonItem(button))

    def get_template_name(self):
        return "social_media_icons.html"


class SocialMediaButtonItem(Item):
    def __init__(self, button):
        self.url = button.url
        self.icon_url = button.get_icon_url()
