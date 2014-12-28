<h1>Logging</h1>
The Python logging module is used for logging. Add and commit plenty of useful log statements. This support effective debugging. 

### Example
To add log statements, simply add the following at the top of your Python file,
```python
import logging
logger = logging.getLogger(__name__)
```
and add a new log statement anywhere in this file by,
```python
logger.debug('debug log statement')
logger.warning('warning message')
logger.error('error message')
```
The log statements include log level, application, class, function and line number of the log statement,
```python
[2014-12-19 22:39:11] ERROR [website.tests::test_logfile() (23)]: Cannot find anything here.
```
### Levels
Five log levels are available, `logger.debug()`, `logger.info()`, `logger.warning()`, `logger.error()`, `logger.critical()`. 

### Output to console and file
The log statements for the applications are written to the console, if DEBUG=True, and always to `debug.log` and `error.log`. Django errors can be found in `django.log`.

### Configuration
Logging is configured in the Django `settings.py` `LOGGING` variables. Information about configuration can be found [here](https://docs.djangoproject.com/en/1.7/topics/logging/). New applications have to be added before logging becomes active for those applications. 

### Confidential information
Confidential information should not be logged. During initial development, logging of confidential information is allowed if marked with a `CONF` tag, `logger.debug('CONF ' + member.DNA)`. These will be removed before deployment.  
