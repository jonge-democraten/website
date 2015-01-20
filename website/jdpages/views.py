import logging
logger = logging.getLogger(__name__)

from django.utils.html import strip_tags


class HorizontalPosition():
    LEFT = 'Left'
    RIGHT = 'Right'
    POSITION_CHOICES = (
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
    )


class Item():
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
