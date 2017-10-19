"""
Default settings for the ``website`` app. Each of these can be
overridden in your project's settings module, just like regular
Django/Mezzanine settings.
"""
from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting

register_setting(
    name="RICHTEXT_SCRIPT_TAG_WHITELIST",
    description=_("A whitelist of allowed script tags. All script tags that "
                  "are not on the list are removed via RICHTEXT_FILTERS."
                  "Used in utils.filters.strip_scripts_not_in_whitelist."),
    editable=False,
    default=(),
)

SIDEBAR_AGENDA_SETTINGS = (
    (1, _("Just this site")),
    (2, _("This site and the main site")),
    (3, _("All sites")),
    (4, _("Main site")),
)

register_setting(
    name="SIDEBAR_AGENDA_SITES",
    description=_("For which sites should events be displayed in the sidebar "
                  "upcoming events listing of this site?"),
    editable=True,
    choices=SIDEBAR_AGENDA_SETTINGS,
    default=2,
)

register_setting(
    name="PIWIK_SITE_ID",
    description=_("The Piwik site ID. This is the ID that is set in Piwik to track this site."),
    editable=True,
    default=1,
)

register_setting(
    name="TWITTER_NAME",
    description=_("The twitter timeline name."),
    editable=True,
    default="JongeDemocraten",
)

# A list of unused Mezzanine settings that should be hidden in the admin
HIDDEN_SETTINGS = (
    'COMMENTS_ACCOUNT_REQUIRED',
    'COMMENTS_DEFAULT_APPROVED',
    'COMMENTS_DISQUS_API_PUBLIC_KEY',
    'COMMENTS_DISQUS_API_SECRET_KEY',
    'COMMENTS_DISQUS_SHORTNAME',
    'COMMENTS_NOTIFICATION_EMAILS',
    'COMMENTS_NUM_LATEST',
    'COMMENTS_REMOVED_VISIBLE',
    'COMMENTS_UNAPPROVED_VISIBLE',
    'COMMENTS_USE_RATINGS',
    'COMMENT_FILTER',
    'AKISMET_API_KEY',
    'BITLY_ACCESS_TOKEN',
    'GOOGLE_ANALYTICS_ID',
    'RATINGS_ACCOUNT_REQUIRED',
    'TAG_CLOUD_SIZES',
)
