from __future__ import absolute_import, unicode_literals

######################
# MEZZANINE SETTINGS #
######################

# The following settings are already defined with default values in
# the ``defaults.py`` module within each of Mezzanine's apps, but are
# common enough to be put here, commented out, for convenient
# overriding. Please consult the settings documentation for a full list
# of settings Mezzanine implements:
# http://mezzanine.jupo.org/docs/configuration.html#default-settings

# Controls the ordering and grouping of the admin menu.
#
ADMIN_MENU_ORDER = (
    ("Content", ("pages.Page", "blog.BlogPost", "events.Event",
        ("Media Library", "fb_browse"), "hemres.Newsletter")),
    ("Site", ("blog.BlogCategory", "sites.Site", "redirects.Redirect", "jdpages.Footer", "jdpages.SocialMediaUrls", "jdpages.OrganisationMember", "jdpages.OrganisationPartMember", "conf.Setting",)),
    ("Users", ("auth.User", "auth.Group", "janeus.JaneusUser", "janeus.JaneusRole", )),

    ("Newsletter templating", ("hemres.NewsletterTemplate")),
    ("Newsletter subscriptions", ("hemres.MailingList", "hemres.EmailSubscriber", "hemres.JaneusSubscriber")),
    ("Sending newsletters", ("hemres.NewsletterToList", "hemres.NewsletterToSubscriber")),
)


# A three item sequence, each containing a sequence of template tags
# used to render the admin dashboard.
#
DASHBOARD_TAGS = (
    ("mezzanine_tags.app_list",),
    ("mezzanine_tags.recent_actions",),
    (),
)

# A sequence of templates used by the ``page_menu`` template tag. Each
# item in the sequence is a three item sequence, containing a unique ID
# for the template, a label for the template, and the template path.
# These templates are then available for selection when editing which
# menus a page should appear in. Note that if a menu template is used
# that doesn't appear in this setting, all pages will appear in it.

PAGE_MENU_TEMPLATES = (
    (1, "Top navigation bar", "pages/menus/jdmenu.html"),
)

# A sequence of fields that will be injected into Mezzanine's (or any
# library's) models. Each item in the sequence is a four item sequence.
# The first two items are the dotted path to the model and its field
# name to be added, and the dotted path to the field class to use for
# the field. The third and fourth items are a sequence of positional
# args and a dictionary of keyword args, to use when creating the
# field instance. When specifying the field class, the path
# ``django.models.db.`` can be omitted for regular Django model fields.
#
# EXTRA_MODEL_FIELDS = (
#     (
#         # Dotted path to field.
#         "mezzanine.blog.models.BlogPost.image",
#         # Dotted path to field class.
#         "somelib.fields.ImageField",
#         # Positional args for field class.
#         ("Image",),
#         # Keyword args for field class.
#         {"blank": True, "upload_to": "blog"},
#     ),
#     # Example of adding a field to *all* of Mezzanine's content types:
#     (
#         "mezzanine.pages.models.Page.another_field",
#         "IntegerField", # 'django.db.models.' is implied if path is omitted.
#         ("Another name",),
#         {"blank": True, "default": 1},
#     ),
# )

# Setting to turn on featured images for blog posts. Defaults to False.
#
BLOG_USE_FEATURED_IMAGE = True

# Models that are included in a search
SEARCH_MODEL_CHOICES = ('pages.Page', 'blog.BlogPost', 'events.Occurrence')

########################
# MAIN DJANGO SETTINGS #
########################

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "nl-NL"

# Supported languages
_ = lambda s: s
LANGUAGES = (
    ('en', _('English')),
)

# A boolean that turns on/off debug mode. When set to ``True``, stack traces
# are displayed for error pages. Should always be set to ``False`` in
# production. Best set to ``True`` in local_settings.py
DEBUG = False

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Tuple of IP addresses, as strings, that:
#   * See debug comments, when DEBUG is true
#   * Receive x-headers
INTERNAL_IPS = ("127.0.0.1",)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

AUTHENTICATION_BACKENDS = ("mezzanine.core.auth_backends.MezzanineBackend", 'janeus.backend.JaneusBackend')

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# The numeric mode to set newly-uploaded files to. The value should be
# a mode you'd pass directly to os.chmod.
FILE_UPLOAD_PERMISSIONS = 0o644

# This setting allows any user with backend access to change or delete any
# blog post by any other user of that site.
OWNABLE_MODELS_ALL_EDITABLE = ('blog.BlogPost',)

# Using this setting, we force every site to use its own directory within
# the Media Library.
MEDIA_LIBRARY_PER_SITE = True


#############
# DATABASES #
#############

DATABASES = {
    "default": {
        # Add "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.",
        # DB name or path to database file if using sqlite3.
        "NAME": "",
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


#########
# PATHS #
#########

import os

# Full filesystem path to the project.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = STATIC_URL + "website/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

# Package/module name to import the root urlpatterns from for the project.
ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

TEMPLATES = [{'APP_DIRS': True,
              'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': (os.path.join(PROJECT_ROOT, "templates"),),
              'OPTIONS': {# Uncomment when moving to Django 1.9
                          #'builtins': ['mezzanine.template.loader_tags'],
                          'context_processors': ('django.contrib.auth.context_processors.auth',
                                                 'django.contrib.messages.context_processors.messages',
                                                 'django.core.context_processors.debug',
                                                 'django.core.context_processors.i18n',
                                                 'django.core.context_processors.static',
                                                 'django.core.context_processors.media',
                                                 'django.core.context_processors.request',
                                                 'django.core.context_processors.tz',
                                                 'mezzanine.conf.context_processors.settings',
                                                 'mezzanine.pages.context_processors.page',
                                                 'website.jdpages.context_processors.site_properties',
                                                 'website.jdpages.context_processors.piwik',
                                                 'website.jdpages.context_processors.homepage_header'),
                          'debug': DEBUG}}]

# This setting replaces the default TinyMCE configuration with our custom
# one. The only difference is that the media plugin is not loaded in default
# version.
TINYMCE_SETUP_JS = STATIC_URL + "website/js/tinymce_setup.js"


################
# APPLICATIONS #
################

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.redirects",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "formtools",
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "captcha",
    "website",
    "website.core",
    "website.jdpages",
    "fullcalendar",
    # "mezzanine.accounts",
    # "mezzanine.mobile",
    "debug_toolbar",
    "janeus",
    "hemres",
    "django_rq",
    "robots",
)

# List of middleware classes to use. Order is important; in the request phase,
# these middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    "mezzanine.core.middleware.UpdateCacheMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.RedirectFallbackMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
)

# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#########################
# OPTIONAL APPLICATIONS #
#########################

# These will be added to ``INSTALLED_APPS``, only if available.
OPTIONAL_APPS = (
    "debug_toolbar",
    "django_extensions",
    "compressor",
    PACKAGE_NAME_FILEBROWSER,
    PACKAGE_NAME_GRAPPELLI,
)

#########################
# LOGGING CONFIGURATION #
#########################

# Directory of the logfiles
LOG_DIR = os.path.join(os.path.dirname(PROJECT_ROOT), 'log')

# Max. logfile size
LOGFILE_MAXSIZE = 10 * 1024 * 1024

# Number of old log files that are stored before they are deleted
# see https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler
LOGFILE_BACKUP_COUNT = 3

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s::%(funcName)s() (%(lineno)s)]: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': "[%(asctime)s] %(levelname)s: %(message)s"
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file_django': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'maxBytes': LOGFILE_MAXSIZE,
            'backupCount': LOGFILE_BACKUP_COUNT,
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file_django', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'ERROR',
        },
        'website': {
            'handlers': ['file_debug', 'file_error', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'janeus': {
            'handlers': ['file_debug', 'file_error', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'hemres': {
            'handlers': ['file_debug', 'file_error', 'console', 'mail_admins'],
            'propagate': True,
            'level': 'DEBUG',
        },
    },
}

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from .local_settings import *
except SystemError as e:  # relative imports do not work when using `manage.py runserver`: (Parent module '' not loaded, cannot perform relative import)
    from local_settings import *
except ImportError as e:
    from local_settings import *


####################
# DYNAMIC SETTINGS #
####################

# set_dynamic_settings() will rewrite globals based on what has been
# defined so far, in order to provide some better defaults where
# applicable. We also allow this settings module to be imported
# without Mezzanine installed, as the case may be when using the
# fabfile, where setting the dynamic settings below isn't strictly
# required.
try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())


#################
# FORM SETTINGS #
#################

# Register the extra form field to store integers (NUMBER stores floats).
FORMS_EXTRA_FIELDS = [
    [
        100, "django.forms.IntegerField", "Integer",
    ],
    [
        101, "captcha.fields.CaptchaField", "CAPTCHA",
    ],
]


##############################
# YOUTUBE EMBEDDING SETTINGS #
##############################

# Could not find a way to append to the default, so we copy the defaults here.
# The defaults are defined in mezzanine/core/defaults.py"
RICHTEXT_ALLOWED_TAGS = (
    "a", "abbr", "acronym", "address", "area", "article", "aside",
    "b", "bdo", "big", "blockquote", "br", "button", "caption", "center",
    "cite", "code", "col", "colgroup", "dd", "del", "dfn", "dir", "div",
    "dl", "dt", "em", "fieldset", "figure", "font", "footer", "form",
    "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "i", "img",
    "input", "ins", "kbd", "label", "legend", "li", "map", "menu",
    "nav", "ol", "optgroup", "option", "p", "pre", "q", "s", "samp",
    "section", "select", "small", "span", "strike", "strong",
    "sub", "sup", "table", "tbody", "td", "textarea",
    "tfoot", "th", "thead", "tr", "tt", "u", "ul", "var", "wbr"
)
# We append iframes to allow Youtube video embedding
RICHTEXT_ALLOWED_TAGS += ("iframe",)

# We disallow all iframes that do not include acceptable content. 
# We first copy the default value (defined in mezzanine/core/defaults.py).
RICHTEXT_FILTERS = ("mezzanine.utils.html.thumbnails",)
# We append a function that strips iframes that do not follow the default format
# for an embedded YouTube video, an OpenStreetMap or other content.
RICHTEXT_FILTERS += ("website.utils.filters.filter_iframes",)


####################################
# SCRIPT TAG WHITELISTING SETTINGS #
####################################

# We allow the script tag in rich text fields.
RICHTEXT_ALLOWED_TAGS += ("script",)

# However, we do apply a filter to check them.
RICHTEXT_FILTERS += ("website.utils.filters.strip_scripts_not_in_whitelist",)

# We only allow whitelisted script tags. The rest is removed.
# This is the whitelist. Only exact matches are allowed.
# Rationale behing whitelist:
# Lines 1-5: department map 'Afdelingen'
RICHTEXT_SCRIPT_TAG_WHITELIST = (
    '<script type="text/javascript" src="/static/website/js/topojson.v0.min.js"></script>',
    '<script type="text/javascript" src="/static/website/js/d3.v3.min.js"></script>',
    '<script type="text/javascript" src="/static/website/js/queue.v1.min.js"></script>',
    '<script type="text/javascript" src="/static/website/js/d3.geo.projection.v0.min.js"></script>',
    '<script type="text/javascript" src="/static/website/js/render.js"></script>',
    '<script type="text/javascript" src="/static/website/js/jdshowhide.js"></script>',
)


##########################
# PDF EMBEDDING SETTINGS #
##########################

# We allow the object tag in rich text fields.
RICHTEXT_ALLOWED_TAGS += ("object",)

# We also need the data attribute, so we copy the default list of allowed
# attributes here and add 'data' (at the end, for clarity).
RICHTEXT_ALLOWED_ATTRIBUTES = ("abbr", "accept", "accept-charset", "accesskey", "action",
    "align", "alt", "axis", "border", "cellpadding", "cellspacing",
    "char", "charoff", "charset", "checked", "cite", "class", "clear",
    "cols", "colspan", "color", "compact", "coords", "datetime", "dir",
    "disabled", "enctype", "for", "frame", "headers", "height", "href",
    "hreflang", "hspace", "id", "ismap", "label", "lang", "longdesc",
    "maxlength", "media", "method", "multiple", "name", "nohref",
    "noshade", "nowrap", "prompt", "readonly", "rel", "rev", "rows",
    "rowspan", "rules", "scope", "selected", "shape", "size", "span",
    "src", "start", "style", "summary", "tabindex", "target", "title",
    "type", "usemap", "valign", "value", "vspace", "width", "xml:lang",
    "data")

# However, we do apply a filter to check them. Only embedding of locally
# hosted PDFs is allowed.
RICHTEXT_FILTERS += ("website.utils.filters.strip_illegal_objects",)

##########################
# MEDIA LIBRARY SETTINGS #
##########################

# We want to also allow uploading of .odt, .ods, .docx and .xlsx files.
# Appending to settings is not possible, so we copy-pasted the default settings
# here and added '.odt', '.ods', '.docx' and '.xlsx'.
#
# Default is available at /filebrowser_safe/settings.py
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Document': ['.pdf', '.doc', '.docx', '.rtf', '.txt', '.xls', '.xlsx',
                 '.csv', '.odt', '.ods'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p'],
    'Code': ['.html', '.py', '.js', '.css']
}

#####################
# TEMPLATE SETTINGS #
#####################

# This is the default list of settings that are accessible to templates, 
# because apparently Mezzanine has difficulty accessing the JQUERY_UI_FILENAME
# setting otherwise.
# This could be a bug in Mezzanine.

TEMPLATE_ACCESSIBLE_SETTINGS = ('ACCOUNTS_APPROVAL_REQUIRED', 'ACCOUNTS_VERIFICATION_REQUIRED', 'ADMIN_MENU_COLLAPSED', 'BITLY_ACCESS_TOKEN', 'BLOG_USE_FEATURED_IMAGE', 'COMMENTS_DISQUS_SHORTNAME', 'COMMENTS_NUM_LATEST', 'COMMENTS_DISQUS_API_PUBLIC_KEY', 'COMMENTS_DISQUS_API_SECRET_KEY', 'COMMENTS_USE_RATINGS', 'DEV_SERVER', 'FORMS_USE_HTML5', 'GRAPPELLI_INSTALLED', 'GOOGLE_ANALYTICS_ID', 'JQUERY_FILENAME', 'JQUERY_UI_FILENAME', 'LOGIN_URL', 'LOGOUT_URL', 'SITE_TITLE', 'SITE_TAGLINE', 'USE_L10N')

TEMPLATE_ACCESSIBLE_SETTINGS += ('PIWIK_SITE_ID',)
TEMPLATE_ACCESSIBLE_SETTINGS += ('TWITTER_NAME',)

###################
# JANEUS SETTINGS #
###################

JANEUS_MEZZANINE_CLEAR_SITEPERMISSION = True

