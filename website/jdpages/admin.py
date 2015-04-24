import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import admin
from django.utils.functional import curry
from django.forms.models import ModelForm

from mezzanine.core.admin import SingletonAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.forms.models import Form
from mezzanine.forms.admin import FormAdmin
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage

from website.jdpages.models import BlogCategoryPage
from website.jdpages.models import ColumnElement, ColumnElementWidget
from website.jdpages.models import DocumentListing, Document
from website.jdpages.models import HomePage
from website.jdpages.models import HorizontalPosition
from website.jdpages.models import PageHeaderImageWidget
from website.jdpages.models import SocialMediaButton
from website.jdpages.models import Sidebar
from website.jdpages.models import SidebarBlogCategoryWidget
from website.jdpages.models import SidebarBannerWidget
from website.jdpages.models import SidebarTabsWidget
from website.jdpages.models import SidebarTwitterWidget


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


class ColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """ Base admin class for a column element """

    model = ColumnElementWidget

    def get_formset(self, request, obj=None, **kwargs):
        """ 
        Adds the initial value of the horizontal position to the formset.
        Note: does not work for the 'Add another' button in the admin.
        """
        initial = [{'horizontal_position': self.get_default_position()}]
        formset = super(ColumnElementWidgetInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset


class LeftColumnElementWidgetInline(ColumnElementWidgetInline):
    """ Inline for a widget in the left column of a column page """

    verbose_name_plural = 'Left column widgets'

    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())

    @staticmethod
    def get_default_position():
        return HorizontalPosition.LEFT


class RightColumnElementWidgetInline(ColumnElementWidgetInline):
    """ Inline for a widget in the right column of a column page """

    verbose_name_plural = 'Right column widgets'

    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())

    @staticmethod
    def get_default_position():
        return HorizontalPosition.RIGHT


class HomePageAdmin(PageAdmin):
    inlines = [PageHeaderImageInline, LeftColumnElementWidgetInline, RightColumnElementWidgetInline]


class RichtTextPageAdmin(PageAdmin):
    inlines = [PageHeaderImageInline, LeftColumnElementWidgetInline, RightColumnElementWidgetInline]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'document_listing')


class ColumnElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'content_type', 'object_id', 'site',)


class ColumnElementWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'column_element', 'page', 'max_items', 'horizontal_position', 'site')


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


class SidebarBlogCategoryWidgetInline(admin.TabularInline):
    model = SidebarBlogCategoryWidget
    extra = 2
    max_num = 2
    verbose_name = "Blogs"
    verbose_name_plural = "Blogs"


class SidebarTwitterWidgetInline(admin.TabularInline):
    model = SidebarTwitterWidget
    verbose_name = "Twitter feed"
    verbose_name_plural = "Twitter feed"


class SidebarTabsWidgetInline(admin.TabularInline):
    model = SidebarTabsWidget
    verbose_name = "Events and newsletter tabs"
    verbose_name_plural = "Events and newsletter tabs"


class SidebarBannerWidgetAdmin(admin.ModelAdmin):
    model = SidebarBannerWidget
    list_display = ('id', 'active', 'title', 'image', 'url')


class SocialMediaButtonInline(TabularDynamicInlineAdmin):
    model = SocialMediaButton
    verbose_name = "Social media buttons"
    verbose_name_plural = "Social media buttons"


class SidebarAdmin(SingletonAdmin):
    model = Sidebar
    inlines = (SidebarBlogCategoryWidgetInline,
               SidebarTwitterWidgetInline,
               SidebarTabsWidgetInline,
               SocialMediaButtonInline,)


class SidebarElementWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'sidebar_element', 'site')


class SocialMediaButtonGroupAdmin(admin.ModelAdmin):
    inlines = (SocialMediaButtonInline,)


admin.site.unregister(RichTextPage)
admin.site.register(RichTextPage, RichtTextPageAdmin)
admin.site.unregister(Form)
admin.site.register(Form, CustomFormAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(BlogCategoryPage, BlogPageAdmin)
admin.site.register(Sidebar, SidebarAdmin)
admin.site.register(SidebarBannerWidget, SidebarBannerWidgetAdmin)
admin.site.register(DocumentListing, DocumentListingAdmin)

# we add some models to the admin for debugging, if we are in debug mode
if settings.DEBUG:
    admin.site.register(ColumnElement, ColumnElementAdmin)
    admin.site.register(ColumnElementWidget, ColumnElementWidgetAdmin)
    admin.site.register(Document, DocumentAdmin)
