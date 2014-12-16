from django.test import TestCase

class TestTest(TestCase):
    def test_asserts(self):
        self.assertTrue(True)
        self.assertEqual(True, True)
        self.assertNotEqual(True, False)
