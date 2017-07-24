import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import admin
from django.forms.models import ModelForm
from django.contrib.admin import TabularInline

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.core.admin import StackedDynamicInlineAdmin
from mezzanine.forms.models import Form
from mezzanine.forms.admin import FormAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.utils.admin import SingletonAdmin

from website.jdpages.models import BlogCategoryPage
from website.jdpages.models import DocumentListing, Document
from website.jdpages.models import HomePage
from website.jdpages.models import VisionPage
from website.jdpages.models import VisionsPage
from website.jdpages.models import ActionBanner
from website.jdpages.models import PageHeaderImageWidget
from website.jdpages.models import SidebarAgenda
from website.jdpages.models import SidebarSocial
from website.jdpages.models import SidebarTwitter
from website.jdpages.models import SidebarLink
from website.jdpages.models import SidebarRichText


class AlwaysChangedModelForm(ModelForm):
    """
    A django modelform that is always changed and will thus always be saved and validated.
    To be used for inlines that should also be created with their default/initial values.
    """
    def has_changed(self):
        """
        Should return True if data differs from initial.
        Unchanged inlines will also get validated and saved by always returning true here.
        """
        return True


class PageHeaderImageInline(TabularDynamicInlineAdmin):
    model = PageHeaderImageWidget
    verbose_name = "Header image"
    verbose_name_plural = "Header images"


class ActionBannerInline(StackedDynamicInlineAdmin):
    model = ActionBanner
    extra = 1
    verbose_name = "Action banner"
    verbose_name_plural = "Action banner"


class SidebarAgendaInline(TabularDynamicInlineAdmin):
    model = SidebarAgenda
    extra = 0
    verbose_name = "Sidebar agenda"
    verbose_name_plural = "Sidebar agenda"


class SidebarSocialInline(TabularDynamicInlineAdmin):
    model = SidebarSocial
    extra = 0
    verbose_name = "Sidebar social"
    verbose_name_plural = "Sidebar social"


class SidebarTwitterInline(TabularDynamicInlineAdmin):
    model = SidebarTwitter
    extra = 0
    verbose_name = "Sidebar twitter"
    verbose_name_plural = "Sidebar twitter"


class SidebarLinkInline(TabularDynamicInlineAdmin):
    model = SidebarLink
    extra = 0
    verbose_name = "Sidebar links"
    verbose_name_plural = "Sidebar links"


class SidebarRichTextInline(TabularDynamicInlineAdmin):
    model = SidebarRichText
    extra = 0
    verbose_name = "Sidebar content"
    verbose_name_plural = "Sidebar content"


class HomePageAdmin(PageAdmin):
    model = HomePage
    inlines = [PageHeaderImageInline, ActionBannerInline, SidebarAgendaInline, SidebarTwitterInline, SidebarSocialInline]


class VisionsPageAdmin(PageAdmin):
    model = VisionsPage
    inlines = [PageHeaderImageInline, ActionBannerInline, SidebarAgendaInline, SidebarTwitterInline, SidebarSocialInline]


class VisionPageAdmin(PageAdmin):
    model = VisionPage
    inlines = [PageHeaderImageInline]


class RichtTextPageAdmin(PageAdmin):
    inlines = [
        PageHeaderImageInline, SidebarAgendaInline, SidebarSocialInline,
        SidebarTwitterInline, SidebarLinkInline, SidebarRichTextInline
    ]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'document_listing')


class BlogPageAdmin(PageAdmin):
    inlines = [PageHeaderImageInline]


class DocumentInline(TabularDynamicInlineAdmin):
    model = Document


class CustomFormAdmin(FormAdmin):
    model = Form
    inlines = [PageHeaderImageInline]
    inlines.insert(0, FormAdmin.inlines[0])


class DocumentListingAdmin(PageAdmin):
    inlines = (DocumentInline, PageHeaderImageInline)


admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, RichtTextPageAdmin)
admin.site.unregister(Form)
admin.site.register(Form, CustomFormAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(VisionPage, VisionPageAdmin)
admin.site.register(VisionsPage, VisionsPageAdmin)
admin.site.register(BlogCategoryPage, BlogPageAdmin)
admin.site.register(DocumentListing, DocumentListingAdmin)

# we add some models to the admin for debugging, if we are in debug mode
if settings.DEBUG:
    admin.site.register(Document, DocumentAdmin)
