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
