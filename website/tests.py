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
