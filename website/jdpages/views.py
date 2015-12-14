import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement, EventColumnElement
from website.jdpages.models import HomePage
from website.jdpages.models import PageHeaderImageWidget
from website.jdpages.models import get_public_blogposts


def create_column_items(column_widgets):
    """ creates view items for the more column widget models """
    column_items = []
    for widget in column_widgets:
        model_class = widget.column_element.content_type.model_class()
        if model_class == BlogCategory:
            blog_category = widget.column_element.get_object()
            if widget.column_element.subtype == ColumnElement.COMPACT:
                column_items.append(BlogCategoryHeadlineColumnItem(blog_category, widget))
            else:
                column_items.append(BlogCategoryColumnItem(blog_category, widget))
        elif model_class == EventColumnElement:
            event_element = widget.column_element.get_object()
            column_items.append(EventColumnItem(event_element, widget))
    return column_items


class Item(object):
    """ A generic view item with a template and all data needed in the template. """
    def __init__(self, title=""):
        self.title = title

    def get_template_name(self):
        return "none"

    def is_blog_category_sidebar_item(self):
        return isinstance(self, BlogCategorySidebarItem)

    def is_social_media_button_group_item(self):
        return isinstance(self, SocialMediaButtonGroupItem)


class BlogCategoryColumnItem(Item):
    """
    Column view item for a mezzanine BlogCategory.
    Has BlogPostItems as children.
    Shows an excerpt of the last n posts.
    """
    def __init__(self, blogcategory, widget):
        super(BlogCategoryColumnItem, self).__init__(widget.title)
        self.url = blogcategory.get_absolute_url()
        self.children = self.create_children(blogcategory, widget.max_items)

    @staticmethod
    def create_children(blogcategory, max_items):
        children = []
        blogposts = get_public_blogposts(blogcategory)[:max_items]
        for post in blogposts:
            children.append(BlogPostItem(post))
        return children

    def get_template_name(self):
        return "blogcategory_column_item.html"


class BlogCategoryHeadlineColumnItem(BlogCategoryColumnItem):
    """ Column view item for a blog category with headlines only. """
    def __init__(self, blogcategory, widget):
        super(BlogCategoryHeadlineColumnItem, self).__init__(blogcategory, widget)

    def get_template_name(self):
        return "blogcategory_compact_column_item.html"


class BlogPostItem(Item):
    """
    BlogPost view item with data needed to render (part of a) blogpost.
    HTML richtext is stripped from the content.
    """
    def __init__(self, blogpost):
        super(BlogPostItem, self).__init__(blogpost.title)
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)


class EventColumnItem(Item):
    """ Column view item for an Event. """
    def __init__(self, event_element, widget):
        super(EventColumnItem, self).__init__(widget.title)
        self.type = event_element.type
        self.max_items = widget.max_items
        self.url = "/events/"

    def get_template_name(self):
        return "events_column_item.html"


class BlogCategorySidebarItem(Item):
    """
    Sidebar view item for a mezzanine BlogCategory.
    Has BlogPostItems as children.
    Shows an excerpt of the last post.
    """
    def __init__(self, blogcategory):
        super(BlogCategorySidebarItem, self).__init__()
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
    """ View item for a list of social media buttons. """
    def __init__(self, buttons):
        super(SocialMediaButtonGroupItem, self).__init__()
        self.children = []
        for button in buttons:
            self.children.append(SocialMediaButtonItem(button))

    def get_template_name(self):
        return "social_media_icons.html"


class SocialMediaButtonItem(Item):
    """ View item for a single social media button, to be shown in a button group. """
    def __init__(self, button):
        super(SocialMediaButtonItem, self).__init__()
        self.url = button.url
        self.icon_url = button.get_icon_url()
        self.media_type = button.get_type_name()

    def mobile_icon_url(self):
        parts = self.icon_url.rsplit('/', 1)
        return "/mobile/".join(parts)


class BannerSidebarItem(Item):
    """ View item for a banner (image) on the sidebar. """
    def __init__(self, widget):
        super(BannerSidebarItem, self).__init__()
        self.image_url = widget.image.url
        self.url = widget.url
        self.description = widget.description

    def get_template_name(self):
        return "banner_sidebar_item.html"


class TwitterSidebarItem(Item):
    """ Sidebar view item for a twitter feed. """
    def get_template_name(self):
        return "twitter_feed_item.html"


class TabsSidebarItem(Item):
    """ Sidebar item for a tabbed view. """
    def get_template_name(self):
        return "tabs_sidebar_item.html"


def get_page_header(page):
    """
    :returns: the page header for a given page.
    Uses parent page image when none is defined.
    Top parent is the HomePage.
    None when there is no Hompage or when the HomePage has no header.
    """

    # Get a random page header, or the first one if there is only one
    image = PageHeaderImageWidget.objects.filter(page=page).order_by('?').first()
    if image is not None:
        return image

    # No image found! If we received an integer, then do not search further
    if isinstance(page, int):
        return None

    # Try from parent
    if page.parent:
        return get_page_header(page.parent)

    # Try from first homepage
    homepage = HomePage.objects.values_list('id').first()
    if len(homepage) != 0:
        # Since we give get_page_header an integer, there is no infinite recursion here...
        return get_page_header(homepage[0])

    return None


def get_homepage_header():
    """ Returns the page header image of the homepage """
    homepage = HomePage.objects.values_list('id').first()
    if len(homepage) == 0:
        return None
    return get_page_header(homepage[0])
