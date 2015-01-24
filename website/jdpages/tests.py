import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement
from website.jdpages.models import SidebarElement
from website.jdpages.models import SidebarBanner
from website.jdpages.models import SocialMediaButtonGroup


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


class TestSidebarElement(TestCase):
    """ SidebarElement test case. """

    def test_auto_create_social_media(self):
        """
        Tests whether a SidebarElement is automatically created
        when a SocialMediaButtonGroup is created, 
        and that the element has a reference to it.
        """
        group = SocialMediaButtonGroup.objects.create(name="Test Button Group")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), group)

    def test_auto_delete_social_media(self):
        """
        Tests whether the related SidebarElement is automatically deleted
        when a SocialMediaButtonGroup is deleted.
        """
        group = SocialMediaButtonGroup.objects.create(name="Test Button Group")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), group)
        group.delete()
        self.assertEqual(SocialMediaButtonGroup.objects.count(), 0)
        self.assertEqual(SidebarElement.objects.count(), 0)

    def test_auto_create_blogcategory(self):
        """
        Tests whether a SidebarElement is automatically created
        when a BlogCategory is created,
        and that the element has a reference to it.
        """
        blogcategory = BlogCategory.objects.create(title="Test BlogCategory")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), blogcategory)

    def test_auto_delete_blogcategory(self):
        """
        Tests whether the related SidebarElement is automatically deleted
        when a BlogCategory is deleted.
        """
        blogcategory = BlogCategory.objects.create(title="Test BlogCategory")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), blogcategory)
        blogcategory.delete()
        self.assertEqual(SocialMediaButtonGroup.objects.count(), 0)
        self.assertEqual(SidebarElement.objects.count(), 0)

    def test_auto_create_banner(self):
        """
        Tests whether a SidebarElement is automatically created
        when a SidebarBanner is created,
        and that the element has a reference to it.
        """
        sidebarbanner = SidebarBanner.objects.create(title="Test Sidebar Banner")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), sidebarbanner)

    def test_auto_delete_banner(self):
        """
        Tests whether the related SidebarElement is automatically deleted
        when a SidebarBanner is deleted.
        """
        sidebarbanner = SidebarBanner.objects.create(title="Test Sidebar Banner")
        self.assertEqual(SidebarElement.objects.count(), 1)
        element = SidebarElement.objects.get(id=1)
        self.assertEqual(element.get_object(), sidebarbanner)
        sidebarbanner.delete()
        self.assertEqual(SocialMediaButtonGroup.objects.count(), 0)
        self.assertEqual(SidebarElement.objects.count(), 0)
