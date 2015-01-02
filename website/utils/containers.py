from django.utils.html import strip_tags


class BlogPostInfo():
    def __init__(self, blogpost):
        self.title = blogpost.title
        self.author = blogpost.user
        self.date = blogpost.publish_date
        self.url = blogpost.get_absolute_url()
        self.content = strip_tags(blogpost.content)
