import datetime

from django.utils.html import strip_tags
from django.utils.safestring import mark_safe


class ColumnItem():
    def get_template_name(self):
        return "none"
        

class BlogPostItem(ColumnItem):
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)
        
    def get_template_name(self):
        return "blogpostitem.html"

