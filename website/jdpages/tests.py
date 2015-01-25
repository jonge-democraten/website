import logging
logger = logging.getLogger(__name__)

from django.test import TestCase
from django.test import Client

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement
from website.jdpages.models import Sidebar
from website.jdpages.views import BlogCategorySidebarItem
from website.jdpages.views import TwitterSidebarItem
from website.jdpages.views import SocialMediaButtonGroupItem


class TestColumnElement(TestCase):
    """ ColumnElement test case. """

    def test_auto_create(self):
        """
        Tests whether a ColumnElement is automatically created
        when a BlogCategory is created, and that the element has a to it.
        """
        category = BlogCategory.objects.create(title="Test Blog")
        self.assertEqual(ColumnElement.objects.count(), 1)
        element = ColumnElement.objects.get(id=1)
        self.assertEqual(element.get_object(), category)

    def test_auto_delete(self):
        """
        Tests whether a ColumnElement is automatically deleted
        when a BlogCategory is deleted.
        """
        category = BlogCategory.objects.create(title="Test Blog")
        self.assertEqual(ColumnElement.objects.count(), 1)
        element = ColumnElement.objects.get(id=1)
        self.assertEqual(element.get_object(), category)
        category.delete()
        self.assertEqual(BlogCategory.objects.count(), 0)
        self.assertEqual(ColumnElement.objects.count(), 0)


class TestSidebar(TestCase):
    """ Tests the sidebar and its widgets. """
    fixtures = ['test_sidebar.json']

    def setUp(self):
        self.client = Client()

    def login(self):
        """ Login as admin. """
        return self.client.post('/admin/login/?next=/admin/', {'username': 'admin', 'password': 'admin'}, follow=True)

    def test_edit_sidebar_admin_view(self):
        """ Tests whether the change sidebar admin view response is OK (200). """
        response = self.login()
        self.assertEqual(response.status_code, 200)
        sidebars = Sidebar.objects.all()
        self.assertEquals(sidebars.count(), 1)
        sidebar = sidebars[0]
        response = self.client.get('/admin/jdpages/sidebar/' + str(sidebar.id) + '/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_items_sidebar(self):
        """ Tests whether the sidebar view items exist in the homepage context. """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        items = response.context['sidebar_items']
        self.assertTrue(type(items[0]) == BlogCategorySidebarItem)
        self.assertTrue(type(items[1]) == TwitterSidebarItem)
        self.assertTrue(type(items[2]) == SocialMediaButtonGroupItem)
