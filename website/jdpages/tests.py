import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from mezzanine.blog.models import BlogCategory

from website.jdpages.models import ColumnElement


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
