import logging
import os

from django.conf import settings
from django.test import TestCase

logger = logging.getLogger(__name__)

class TestTest(TestCase):
    def test_asserts(self):
        self.assertTrue(True)
        self.assertEqual(True, True)
        self.assertNotEqual(True, False)

class TestLogging(TestCase):
    def test_logfile(self):
        debug_message = 'test debug log message'
        logger.debug(debug_message)
        logger.info('test info log message')
        logger.warning('test warning log message')
        
        error_message = 'test error log message'
        logger.error(error_message)
        logger.critical('test critical log message')
        
        debuglog_path = os.path.join(settings.LOG_DIR, 'debug.log')
        self.assertTrue( os.path.isfile(debuglog_path) )

        errorlog_path = os.path.join(settings.LOG_DIR, 'error.log')
        self.assertTrue( os.path.isfile(errorlog_path) )
        
        with open(debuglog_path, 'r') as file_debug:
            logfile_str = file_debug.read()
            self.assertTrue( logfile_str.find(debug_message) != -1 )
            self.assertTrue( logfile_str.find(error_message) != -1 )

        with open(errorlog_path, 'r') as file_error:
            logfile_str = file_error.read()
            self.assertTrue( logfile_str.find(debug_message) == -1 )
            self.assertTrue( logfile_str.find(error_message) != -1 )
