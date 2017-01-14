########################
# MAIN DJANGO SETTINGS #
########################

DEBUG = True

# People who get code error notifications.
# In the format (('Full Name', 'email@example.com'),
#                ('Full Name', 'anotheremail@example.com'))
ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# SECURITY WARNING: Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TIME_ZONE = "Europe/Amsterdam"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'jd.local', 'lh.jd.local', 'ams.jd.local']

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.sqlite3",
        # DB name or path to database file if using sqlite3.
        "NAME": "dev.db",
        # Not used with sqlite3.
        "USER": "",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "",
    }
}

USE_L10N = True
LANGUAGE_CODE = "en-US"

###################
# JANEUS SETTINGS #
###################

# Remove this when you set JANEUS_SERVER, JANEUS_DN and JANEUS_PASS
def JANEUS_FAKE_LDAP(username, password):
    # user "someuser" with password "somepass" has groups "role1" and "role2"
    example_users = {"someuser": ("somepass", ["role1", "role2"])}
    if username not in example_users:
        return None
    pwd, groups = example_users[username]
    if password is None or password == pwd:
        return groups
    return None

# JANEUS_SERVER = "ldap://127.0.0.1:389/"
# JANEUS_DN = "dnoftheuser"
# JANEUS_PASS = "thisisaverysecretpassword"

###################
# HEMRES SETTINGS #
###################

# Redis queues for Hemres. Hemres uses "default" queue for sending newsletters.
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    },
}

##################
# PIWIK SETTINGS #
##################

# The Piwik URL, including trailing slash, this is where your Piwik instance is running.
# Remove/comment this setting, or set an empty URL, to disable Piwik tracking.
PIWIK_URL = '127.0.0.1/piwik/'

############################
# EMAIL ERROR NOTIFICATION #
############################

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.domain.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
# Default email address to use for various automated correspondence from the site manager(s).
DEFAULT_FROM_EMAIL = 'info@domain.com'
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
SERVER_EMAIL = 'error@domain.com'
# Subject-line prefix for email messages sent with django.core.mail.mail_admins or django.core.mail.mail_managers.
EMAIL_SUBJECT_PREFIX = '[jdwebsite error] '

#########################
# FULLCALENDAR SETTINGS #
#########################

FULLCALENDAR_SITE_COLORS = {
    1: 'green',
    2: 'red',
    3: ('white', 'black', 'black'),
}
