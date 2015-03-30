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


class Item(object):
    def get_template_name(self):
        return "none"

    def is_blog_category_sidebar_item(self):
        return isinstance(self, BlogCategorySidebarItem)

    def is_social_media_button_group_item(self):
        return isinstance(self, SocialMediaButtonGroupItem)


class BlogCategoryItem(Item):
    def __init__(self, blogcategory, max_posts):
        self.title = blogcategory.title
        self.url = blogcategory.get_absolute_url()
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


class BlogPostItem(Item):
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)


class BlogCategorySidebarItem(Item):
    def __init__(self, blogcategory):
        self.children = self.create_children(blogcategory)

    @staticmethod
    def create_children(blogcategory):
        children = []
        blogposts = get_public_blogposts(blogcategory)[:1]
        for post in blogposts:
            children.append(BlogPostItem(post))
        return children

    def get_template_name(self):
        return "blogpost_sidebar_item.html"


class SocialMediaButtonGroupItem(Item):
    def __init__(self, buttons):
        self.children = []
        for button in buttons:
            self.children.append(SocialMediaButtonItem(button))

    def get_template_name(self):
        return "social_media_icons.html"


class SocialMediaButtonItem(Item):
    def __init__(self, button):
        self.url = button.url
        self.icon_url = button.get_icon_url()
        self.media_type = button.get_type_name()

    def mobile_icon_url(self):
        parts = self.icon_url.rsplit('/', 1)
        return "/mobile/".join(parts)


class BannerSidebarItem(Item):
    def __init__(self, widget):
        self.image_url = widget.image.url
        self.url = widget.url
        self.description = widget.description

    def get_template_name(self):
        return "banner_sidebar_item.html"


class TwitterSidebarItem(Item):
    def get_template_name(self):
        return "twitter_feed_item.html"

class TabsSidebarItem(Item):
    def get_template_name(self):
        return "tabs_sidebar_item.html"
