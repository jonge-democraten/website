import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement, EventColumnElement
from website.jdpages.models import HomePage
from website.jdpages.models import PageHeaderImageWidget
from website.jdpages.models import get_public_blogposts


def create_column_items(column_widgets):
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
    def __init__(self, title=""):
        self.title = title

    def get_template_name(self):
        return "none"

    def is_blog_category_sidebar_item(self):
        return isinstance(self, BlogCategorySidebarItem)

    def is_social_media_button_group_item(self):
        return isinstance(self, SocialMediaButtonGroupItem)


class BlogCategoryColumnItem(Item):
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
    def __init__(self, blogcategory, widget):
        super(BlogCategoryHeadlineColumnItem, self).__init__(blogcategory, widget)

    def get_template_name(self):
        return "blogcategory_compact_column_item.html"


class BlogPostItem(Item):
    def __init__(self, blogpost):
        super(BlogPostItem, self).__init__(blogpost.title)
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)


class EventColumnItem(Item):
    def __init__(self, event_element, widget):
        super(EventColumnItem, self).__init__(widget.title)
        self.type = event_element.type
        self.max_items = widget.max_items

    def get_template_name(self):
        return "events_column_item.html"


class BlogCategorySidebarItem(Item):
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
    def __init__(self, buttons):
        super(SocialMediaButtonGroupItem, self).__init__()
        self.children = []
        for button in buttons:
            self.children.append(SocialMediaButtonItem(button))

    def get_template_name(self):
        return "social_media_icons.html"


class SocialMediaButtonItem(Item):
    def __init__(self, button):
        super(SocialMediaButtonItem, self).__init__()
        self.url = button.url
        self.icon_url = button.get_icon_url()
        self.media_type = button.get_type_name()

    def mobile_icon_url(self):
        parts = self.icon_url.rsplit('/', 1)
        return "/mobile/".join(parts)


class BannerSidebarItem(Item):
    def __init__(self, widget):
        super(BannerSidebarItem, self).__init__()
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


def get_page_header(page):
    page_header_images = PageHeaderImageWidget.objects.filter(page=page)

    n_images = page_header_images.count()
    if n_images == 1:
        return get_first_page_header(page)
    elif n_images == 0:
        if page.parent:
            return get_page_header(page.parent)
        else:
            homepages = HomePage.objects.all()
            if not homepages.exists():
                return None
            elif page == homepages[0]:  # prevent infinite recursion
                return None
            elif PageHeaderImageWidget.objects.filter(page=homepages[0]):
                return get_page_header(homepages[0])
    elif n_images > 1:
        return get_random_page_header(page)


def get_first_page_header(page):
    page_header = PageHeaderImageWidget.objects.filter(page=page)
    if page_header.exists():
        return page_header[0]
    else:
        return None


def get_random_page_header(page):
    page_header = PageHeaderImageWidget.objects.filter(page=page)
    if page_header.exists():
        return PageHeaderImageWidget.objects.filter(page=page).order_by('?')[0]
    return None