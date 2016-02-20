"""
Unit tests for general project functionality.
"""

import datetime
import logging
import os

from django.conf import settings
from django.test import TestCase

logger = logging.getLogger(__name__)


class TestTest(TestCase):
    """ Example test case. """

    def test_asserts(self):
        """ Example unit test. Tests unittest asserts. """
        self.assertTrue(True)
        self.assertEqual(True, True)
        self.assertNotEqual(True, False)


class TestLogging(TestCase):
    """ Unit tests for logging. """

    def test_logfile(self):
        """
        Tests that debug and error log files are created
        and that they contain the test log statement.
        """
        debug_message = 'test debug log statement'
        debug_message += str(datetime.datetime.now())
        logger.debug(debug_message)
        logger.info('test info log message')
        logger.warning('test warning log message')
        error_message = 'test error log message'
        error_message += str(datetime.datetime.now())
        logger.error(error_message)
        logger.critical('test critical log message')

        # assert that the files exist
        debuglog_path = os.path.join(settings.LOG_DIR, 'debug.log')
        self.assertTrue(os.path.isfile(debuglog_path))
        errorlog_path = os.path.join(settings.LOG_DIR, 'error.log')
        self.assertTrue(os.path.isfile(errorlog_path))

        # assert that the log statements are in the files
        with open(debuglog_path, 'r') as file_debug:
            logfile_str = file_debug.read()
            self.assertTrue(logfile_str.find(debug_message) != -1)
            self.assertTrue(logfile_str.find(error_message) != -1)

        with open(errorlog_path, 'r') as file_error:
            logfile_str = file_error.read()
            self.assertTrue(logfile_str.find(debug_message) == -1)
            self.assertTrue(logfile_str.find(error_message) != -1)


class TestIframeStripping(TestCase):
    """
    Unit tests for iframe stripping (only allow YouTube video embedding).
    Tests the accuracy of website.utils.filters.filter_non_video_iframes.
    """
    def test_youtube_not_stripped(self):
        """
        Test whether an iframe containing an embedded YouTube
        video is indeed not stripped when passed through the filter.
        """
        from bs4 import BeautifulSoup as bs
        from website.utils.filters import filter_non_video_iframes

        self.maxDiff = None
        field_value = """
        <div id="test">
<p>Wit amet interdum dolor felis ut ante. Morbi a facilisis ante, in lobortis urna. Etiam ut nunc quis libero interdum aliquam eu at magna. Nunc vehicula risus eleifend molestie vulputate. Mauris diam odio, congue eget lorem id, finibus imperdiet sem.</p>
<p><iframe height="315" src="//www.youtube.com/embed/-Y6ImGzTF70" width="560"></iframe></p>
<p>Vestibulum eget posuere metus, vel finibus leo. Suspendisse congue orci magna, in vestibulum lacus pulvinar a. Donec egestas, felis id feugiat tempus, orci velit ullamcorper risus, et ultricies augue arcu ullamcorper dolor. Mauris eget sollicitudin purus. Aenean a cursus risus, sit amet mattis erat. Curabitur vel venenatis sem. Cras non gravida tellus, eu egestas tellus. Morbi at lorem a turpis blandit vulputate vitae a est.</p></div>
        """
        field_value_post = """
        <div id="test">
<p>Wit amet interdum dolor felis ut ante. Morbi a facilisis ante, in lobortis urna. Etiam ut nunc quis libero interdum aliquam eu at magna. Nunc vehicula risus eleifend molestie vulputate. Mauris diam odio, congue eget lorem id, finibus imperdiet sem.</p>
<p><iframe height="315" src="https://www.youtube-nocookie.com/embed/-Y6ImGzTF70" width="560"></iframe></p>
<p>Vestibulum eget posuere metus, vel finibus leo. Suspendisse congue orci magna, in vestibulum lacus pulvinar a. Donec egestas, felis id feugiat tempus, orci velit ullamcorper risus, et ultricies augue arcu ullamcorper dolor. Mauris eget sollicitudin purus. Aenean a cursus risus, sit amet mattis erat. Curabitur vel venenatis sem. Cras non gravida tellus, eu egestas tellus. Morbi at lorem a turpis blandit vulputate vitae a est.</p></div>
        """

        self.assertEqual(str(bs(field_value_post, 'html.parser')),
                         filter_non_video_iframes(field_value))

    def test_vimeo_stripped(self):
        """
        Test whether a video from a non-YouTube site is stripped
        when passed through the filter.
        """
        from bs4 import BeautifulSoup as bs
        from website.utils.filters import filter_non_video_iframes
        field_value = """
        <div id="test">
<p>Wit amet interdum dolor felis ut ante. Morbi a facilisis ante, in lobortis urna. Etiam ut nunc quis libero interdum aliquam eu at magna. Nunc vehicula risus eleifend molestie vulputate. Mauris diam odio, congue eget lorem id, finibus imperdiet sem.</p>
<iframe src="//player.vimeo.com/video/114963142?byline=0&amp;portrait=0&amp;color=ff0179" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe><p><a href="http://vimeo.com/114963142">IONIAN</a> from <a href="http://vimeo.com/ryanclarke">Ryan Clarke</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
<p>Vestibulum eget posuere metus, vel finibus leo. Suspendisse congue orci magna, in vestibulum lacus pulvinar a. Donec egestas, felis id feugiat tempus, orci velit ullamcorper risus, et ultricies augue arcu ullamcorper dolor. Mauris eget sollicitudin purus. Aenean a cursus risus, sit amet mattis erat. Curabitur vel venenatis sem. Cras non gravida tellus, eu egestas tellus. Morbi at lorem a turpis blandit vulputate vitae a est.</p></div>
        """
        field_value_stripped = """
        <div id="test">
<p>Wit amet interdum dolor felis ut ante. Morbi a facilisis ante, in lobortis urna. Etiam ut nunc quis libero interdum aliquam eu at magna. Nunc vehicula risus eleifend molestie vulputate. Mauris diam odio, congue eget lorem id, finibus imperdiet sem.</p>
<p><a href="http://vimeo.com/114963142">IONIAN</a> from <a href="http://vimeo.com/ryanclarke">Ryan Clarke</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
<p>Vestibulum eget posuere metus, vel finibus leo. Suspendisse congue orci magna, in vestibulum lacus pulvinar a. Donec egestas, felis id feugiat tempus, orci velit ullamcorper risus, et ultricies augue arcu ullamcorper dolor. Mauris eget sollicitudin purus. Aenean a cursus risus, sit amet mattis erat. Curabitur vel venenatis sem. Cras non gravida tellus, eu egestas tellus. Morbi at lorem a turpis blandit vulputate vitae a est.</p></div>
        """
        self.assertEqual(str(bs(field_value_stripped, 'html.parser')),
                         filter_non_video_iframes(field_value))

    def test_nonstandard_youtube_stripped(self):
        """
        Test whether an embedded YouTube video that does not follow
        the standard options gets stripped as well.
        """
        from bs4 import BeautifulSoup as bs
        from website.utils.filters import filter_non_video_iframes
        self.maxDiff = None
        field_value_pre = """<div id="test">
<p>Wit amet interdum dolor felis ut ante. Morbi a facilisis ante, in lobortis urna. Etiam ut nunc quis libero interdum aliquam eu at magna. Nunc vehicula risus eleifend molestie vulputate. Mauris diam odio, congue eget lorem id, finibus imperdiet sem.</p>"""
        field_value_post = """<p>Vestibulum eget posuere metus, vel finibus leo. Suspendisse congue orci magna, in vestibulum lacus pulvinar a. Donec egestas, felis id feugiat tempus, orci velit ullamcorper risus, et ultricies augue arcu ullamcorper dolor. Mauris eget sollicitudin purus. Aenean a cursus risus, sit amet mattis erat. Curabitur vel venenatis sem. Cras non gravida tellus, eu egestas tellus. Morbi at lorem a turpis blandit vulputate vitae a est.</p></div>"""

        # First case: embed from a different URL
        field_value_different_src = field_value_pre + \
            """<iframe width="560" height="315" src="//www.youtub.com/embed/-Y6ImGzTF70"></iframe>""" + \
            field_value_post
        self.assertEqual(str(bs(field_value_pre + field_value_post, 'html.parser')),
                         filter_non_video_iframes(field_value_different_src))

        # Second case: embed using an attribute other than
        # the ones YouTube sets by default (width, height, src,
        # frameborders, allowfullscreen)
        field_value_different_attributes = field_value_pre + \
            """<iframe id="nonstandard" width="560" height="315" src="//www.youtube.com/embed/-Y6ImGzTF70"></iframe>""" + \
            field_value_post
        self.assertEqual(str(bs(field_value_pre + field_value_post, 'html.parser')),
                         filter_non_video_iframes(field_value_different_attributes))

        # Third case: iframe contains information.
        field_value_iframe_has_content = field_value_pre + \
            """<iframe width="560" height="315" src="//www.youtube.com/embed/-Y6ImGzTF70">Test Information</iframe>""" + \
            field_value_post
        self.assertEqual(str(bs(field_value_pre + field_value_post, 'html.parser')),
                         filter_non_video_iframes(field_value_iframe_has_content))


class TestScriptTagWhitelisting(TestCase):
    """
    Unit tests for script tag whitelisting functionality. Tests the accuracy of
    website.utils.filters.strip_scripts_not_in_whitelist.
    """
    from mezzanine.conf import settings

    whitelist = settings.RICHTEXT_SCRIPT_TAG_WHITELIST

    evil_html = """
    This is inconspicuous text that contains evil JavaScript.<script src="http://ev.il/code.js"></script>"""

    evil_html_stripped = """
    This is inconspicuous text that contains evil JavaScript."""

    good_html = """
    This is nice text that contains JavaScript. But don't worry:
    it's all good because it was whitelisted.
    """

    if len(whitelist) > 0:
        good_html += whitelist[0]

    boring_html = """
    This is nice but boring text. It contains another tag, but no scripts.
    <p>This is a separate paragraph.</p>
    """

    def test_evil_is_stripped(self):
        """ Test if an evil script tag is indeed stripped. """
        from website.utils.filters import strip_scripts_not_in_whitelist
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_scripts_not_in_whitelist(self.evil_html),
                         str(bs(self.evil_html_stripped, 'html.parser')))

    def test_good_is_not_stripped(self):
        """ Test if a whitelisted script tag indeed passes unstripped. """
        from website.utils.filters import strip_scripts_not_in_whitelist
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_scripts_not_in_whitelist(self.good_html),
                         str(bs(self.good_html, 'html.parser')))

    def test_boring_is_unchanged(self):
        """ Test if an irrelevant HTML tag passes unstripped. """
        from website.utils.filters import strip_scripts_not_in_whitelist
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_scripts_not_in_whitelist(self.boring_html),
                         str(bs(self.boring_html, 'html.parser')))


class TestObjectFiltering(TestCase):
    """
    Unit tests for PDF embedding functionality. Tests the accuracy of
    website.utils.filters.strip_illegal_objects.
    """
    from mezzanine.conf import settings

    evil_html1 = """
    This is inconspicuous text that contains an evil PDF from an external website.<object data="http://ev.il/my.pdf" type="application/pdf" width="300" height="200">
    Alt text
    </object>"""

    evil_html2 = """
    This is inconspicuous text that contains an evil PDF from an external website.<object data="{0}my.pdf" type="application/doc" width="300" height="200">
    Alt text
    </object>""".format(settings.MEDIA_URL)

    evil_html3 = """
    This is inconspicuous text that contains an evil PDF from an external website.<object data="{0}my.pdf" type="application/pdf" illegal="true" width="300" height="200">
    Alt text
    </object>""".format(settings.MEDIA_URL)

    evil_html_stripped = """
    This is inconspicuous text that contains an evil PDF from an external website."""

    good_html = """
    This is nice text that contains an embedded local PDF.
    <object data="{0}uploads/site-1/documents/doc.pdf" type="application/pdf" width="300" height="200">
    alt text
    </object>
    """.format(settings.MEDIA_URL)

    boring_html = """
    This is nice but boring text. It contains another tag, but no objects.
    <p>This is a separate paragraph.</p>
    """

    def test_evil_domain_is_stripped(self):
        """ Test if an object tag to an external domain is indeed stripped. """
        from website.utils.filters import strip_illegal_objects
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_illegal_objects(self.evil_html1),
            str(bs(self.evil_html_stripped, 'html.parser')))

    def test_evil_filetype_is_stripped(self):
        """ Test if an object tag with an illegal filetype is indeed stripped. """
        from website.utils.filters import strip_illegal_objects
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_illegal_objects(self.evil_html2),
            str(bs(self.evil_html_stripped, 'html.parser')))

    def test_evil_attribute_is_stripped(self):
        """ Test if an object tag with an illegal attribute is indeed stripped. """
        from website.utils.filters import strip_illegal_objects
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_illegal_objects(self.evil_html3),
            str(bs(self.evil_html_stripped, 'html.parser')))

    def test_good_is_not_stripped(self):
        """ Test if a legal object tag indeed passes unstripped. """
        from website.utils.filters import strip_illegal_objects
        from bs4 import BeautifulSoup as bs

        self.assertEqual(strip_illegal_objects(self.good_html),
            str(bs(self.good_html, 'html.parser')))

    def test_boring_is_unchanged(self):
        """ Test if an irrelevant HTML tag passes unstripped. """
        from website.utils.filters import strip_illegal_objects
        from bs4 import BeautifulSoup as bs
 
        self.assertEqual(strip_illegal_objects(self.boring_html),
            str(bs(self.boring_html, 'html.parser')))


class TestJaneus(TestCase):
    """ Test Janeus integration """

    def test_no_access_by_default(self):
        from janeus.backend import JaneusBackend
        self.assertTrue(JaneusBackend().authenticate("someuser", "somepass") is None)

    def test_access_after_role(self):
        from janeus.models import JaneusRole
        role = JaneusRole(role="role1")
        role.save()

        from janeus.backend import JaneusBackend
        user = JaneusBackend().authenticate("someuser", "somepass")
        self.assertTrue(user is not None)
        self.assertTrue(user.user_permissions.count() == 0)

    def test_permissions(self):
        from janeus.models import JaneusRole
        role = JaneusRole(role="role1")
        role.save()

        from django.contrib.auth.models import Permission
        role.permissions.add(*Permission.objects.all())

        from janeus.backend import JaneusBackend
        user = JaneusBackend().authenticate("someuser", "somepass")
        self.assertTrue(user is not None)
        self.assertTrue(len(user.get_all_permissions()) == Permission.objects.count())
