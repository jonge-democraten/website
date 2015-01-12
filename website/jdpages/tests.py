import logging
logger = logging.getLogger(__name__)

from django.test import TestCase

from mezzanine.blog.models import BlogCategory

from .models import ColumnElement


class ColumnElementTest(TestCase):
    """ ColumnElement test case. """

    def test_auto_create(self):
        """
        Tests whether a ColumnElement is automatically created
        when a BlogCategory is created, and that the elements
        has a reference to the new blog category.
        """
        category = BlogCategory.objects.create(title="Test Blog")
        self.assertEqual(ColumnElement.objects.count(), 1)
        element = ColumnElement.objects.get(id=1)
        self.assertEqual(element.get_object(), category)
