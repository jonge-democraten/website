import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test import Client

from mezzanine.blog.models import BlogCategory
from mezzanine.blog.models import BlogPost
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED, CONTENT_STATUS_DRAFT
from mezzanine.pages.models import RichTextPage

from fullcalendar.models import Occurrence


class TestCaseAdminLogin(TestCase):
    """ Test case with client and login as admin function. """

    def setUp(self):
        # Needed during tests with DEBUG=False (the default)
        # to prevent a TemplateDoesNotExist error of a filebrowser template.
        # Not sure what goes wrong here, but seems to work fine in manual tests.
        settings.TEMPLATE_DEBUG = False
        self.client = Client()
        self.login()

    def login(self):
        """ Login as admin. """
        response = self.client.post('/admin/login/?next=/admin/', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)
        return response


class TestPage(TestCaseAdminLogin):
    """ Tests the basic page structure and admin. """
    fixtures = ['test_pages.json']

    def test_edit_richtextpage_admin_view(self):
        richtextpages = RichTextPage.objects.all()
        self.assertEqual(len(richtextpages), 6)
        for page in richtextpages:
            response = self.client.get('/admin/pages/richtextpage/' + str(page.id) + '/', follow=True)
            self.assertEqual(response.status_code, 200)

    def test_richtextpage_view(self):
        richtextpages = RichTextPage.objects.all()
        for page in richtextpages:
            response = self.client.get(page.get_absolute_url(), follow=True)
            self.assertEqual(response.status_code, 200)


class TestPageHeaderImage(TestCaseAdminLogin):
    """ Tests the header image of pages. """
    fixtures = ['test_pages.json']

    def test_edit_header_admin_view(self):
        richtextpages = RichTextPage.objects.all()
        for page in richtextpages:
            response = self.client.get('/admin/pages/richtextpage/' + str(page.id) + '/', follow=True)
            self.assertEqual(response.status_code, 200)

    def test_header_page_view(self):
        richtextpages = RichTextPage.objects.all()
        for page in richtextpages:
            response = self.client.get(page.get_absolute_url(), follow=True)
            self.assertEqual(response.status_code, 200)
            page_header_image_widget = response.context['page_header']
            if page.id == 4:
                self.assertEqual(page_header_image_widget.page.id, 2)
                self.assertEqual(str(page_header_image_widget.image), 'uploads/site-1/example_header.jpg')
            if page.id == 3:
                self.assertEqual(page_header_image_widget.page.id, 2)
                self.assertEqual(str(page_header_image_widget.image), 'uploads/site-1/example_header.jpg')
            if page.id == 8:
                self.assertEqual(page_header_image_widget.page.id, 8)
                self.assertEqual(str(page_header_image_widget.image), 'uploads/site-1/example_header_subpage.jpg')


class TestBlogCategoryPage(TestCaseAdminLogin):
    """ Tests the blog category page rendering """
    fixtures = ['test_blog.json']
    blog_cat_1 = 'BlogCategory1'
    blog_cat_2 = 'BlogCategory2'

    def test_active_in_menu(self):
        """ Tests whether the page is part of the menu. """
        response = self.client.get('/')
        html = str(response.content)
        self.assertTrue('<a href="/blogcategory1page/">BlogCategory1Page</a>' in html)
        self.assertTrue('<a href="/blogcategory2page/">BlogCategory2Page</a>' in html)

    def test_blogpost_titles(self):
        """  Tests whether the blog post titles are shown on a blog category page. """
        response = self.client.get('/blogcategory1page/', follow=True)
        html = str(response.content)
        self.assertTrue('<a href="/blog/blogpost3category1/">BlogPost3Category1</a>' in html)
        self.assertTrue('<a href="/blog/blogpost2category1/">BlogPost2Category1</a>' in html)

    def test_blogpost_contents(self):
        """ Tests whether the blog post contents are shown on the page. """
        response = self.client.get('/blogcategory1page/', follow=True)
        html = str(response.content)
        self.assertTrue('<p>Example content 3.</p>' in html)
        self.assertTrue('<p>Example content 2.</p>' in html)

    def test_blogpage_pagination(self):
        """ Tests whether only a limited number of posts are shown on a page and pagination links are available. """
        response = self.client.get('/blogcategory1page/', follow=True)
        html = str(response.content)
        # the number of posts per pages is set to 2 in the fixtures
        self.assertFalse('<a href="/blog/blogpost1category1/">BlogPost1Category1</a>' in html)
        blog_posts = response.context['blog_posts']
        self.assertEqual(len(blog_posts), 2)
        self.assertTrue('<span>Page 1 of 2</span>' in html)


class TestBlogListView(TestCaseAdminLogin):
    """ Tests the blog post list view. """
    fixtures = ['test_blog.json']
    blog_cat_1 = 'BlogCategory1'
    blog_cat_2 = 'BlogCategory2'
    posts_per_page = 2

    def test_blogpost_titles(self):
        """ Tests whether the titles of the last 2 blog posts are shown on the page. """
        blog_categories = BlogCategory.objects.all()
        for category in blog_categories:
            url = category.get_absolute_url()
            response = self.client.get(url)
            html = str(response.content)
            posts = BlogPost.objects.filter(categories=category)
            counter = 0
            for post in posts:
                post_title_html = '<a href="' + post.get_absolute_url() + '">' + post.title + '</a>'
                if counter < self.posts_per_page:
                    self.assertTrue(post_title_html in html)
                else:
                    self.assertFalse(post_title_html in html)
                counter += 1


class TestEvent(object):
    """
    Tests the integration with the fullcalendar app.
    Tests the events column and sidebar widget, and the individual occurrence page.
    Tests whether the events from the chosen (in the admin) sites are shown,
     * Events from all sites in column element
     * Events from this site in column element
     * Events from this site and main site in column element
    """

    def get_html(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        return str(response.content)

    def test_all_site_events_visibility__user(self):
        """
        Tests whether the events column elements, that is set to show events from all sites,
        actually shows these events,and whether the draft status of events is respected and thus not shown,
        """
        url = '/'
        html = self.get_html(url)
        occurrences = Occurrence.objects.all()
        self.check_occurrence_visibility(occurrences, html, self.is_admin())

    def test_this_site_events_visibility_user(self):
        """
        Tests whether the events column elements, that is set to show events from this site only,
        actually shows only these events, and whether the draft status of events is respected and thus not shown,
        """
        url = '/eventsthissite/'
        html = self.get_html(url)
        occurrences = Occurrence.site_related.all()
        self.check_occurrence_visibility(occurrences, html, self.is_admin())

    def test_this_site_and_main_events_visibility_user(self):
        """
        Tests whether the events column elements, that is set to show events from this and main site,
        actually shows only these events, and whether the draft status of events is respected and thus not shown,
        """
        settings.SITE_ID = 2  # set to a department site
        url = '/'
        html = self.get_html(url)
        sites = {1, 2}
        occurrences = Occurrence.site_related.filter(site_id__in=sites)
        self.check_occurrence_visibility(occurrences, html, self.is_admin())
        occurrences_site_3 = Occurrence.objects.filter(site_id=3)
        for occurrence in occurrences_site_3:
            self.assertFalse(str(occurrence.event.title) in html)
        settings.SITE_ID = 1  # back to main site

    def check_occurrence_visibility(self, occurrences, html, is_admin):
        """
        Tests that draft occurrences are not shown in columns, and that their pages are hidden.
        :param occurrences: the occurrences to check for visibility based on published status
        :param html: the html of the page
        """
        for occurrence in occurrences:
            if occurrence.status == CONTENT_STATUS_DRAFT and not is_admin:
                self.assertFalse(str(occurrence.event.title) in html)
                response = self.client.get(occurrence.get_absolute_url(), follow=True)
                self.assertEqual(response.status_code, 404)
            elif occurrence.status == CONTENT_STATUS_PUBLISHED:
                self.assertTrue(str(occurrence.event.title) in html)
                response = self.client.get(occurrence.get_absolute_url())
                self.assertEqual(response.status_code, 200)


class TestEventAdmin(TestCase, TestEvent):
    """
    Tests the draft/published status visibility in widgets and the occurrence page, for a normal user (draft hidden).
    see TestEvent for actual tests
    """
    fixtures = ['test_events.json']

    def setUp(self):
        self.client = Client()
        response = self.client.post('/admin/login/?next=/admin/', {'username': 'admin', 'password': 'admin'}, follow=True)
        self.assertEqual(response.status_code, 200)

    def is_admin(self):
        return True


class TestEventUser(TestCase, TestEvent):
    """
    Tests the draft/published status visibility in widgets and occurrence page, for an admin (draft visible)
    see TestEvent for actual tests
    """
    fixtures = ['test_events.json']

    def setUp(self):
        self.client = Client()

    def is_admin(self):
        return False
