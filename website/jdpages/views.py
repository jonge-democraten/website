import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from website.jdpages.models import get_public_blogposts


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
