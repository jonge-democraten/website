import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import admin
from django.utils.functional import curry

from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.pages.admin import PageAdmin

from website.jdpages.models import ColumnElement, ColumnElementWidget
from website.jdpages.models import DocumentListing, Document
from website.jdpages.models import HomePage
from website.jdpages.models import HorizontalPosition
from website.jdpages.models import SocialMediaButton
from website.jdpages.models import Sidebar
from website.jdpages.models import SidebarBlogCategoryWidget, SidebarBannerWidget
from website.jdpages.models import SidebarTwitterWidget


class ColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """ """
    model = ColumnElementWidget

    def get_formset(self, request, obj=None, **kwargs):
        """ 
        Adds the initial value of the horizontal position to the formset.
        Note: does not work for the 'Add another' button in the admin.
        """
        initial = []
        initial.append({'horizontal_position': self.get_default_position(),})
        formset = super(ColumnElementWidgetInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        return formset


class LeftColumnElementWidgetInline(ColumnElementWidgetInline):
    """ """
    verbose_name_plural = 'Left column widgets'

    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())

    @staticmethod
    def get_default_position():
        return HorizontalPosition.LEFT


class RightColumnElementWidgetInline(ColumnElementWidgetInline):
    """ """
    verbose_name_plural = 'Right column widgets'
    
    def get_queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=self.get_default_position())

    @staticmethod
    def get_default_position():
        return HorizontalPosition.RIGHT


class HomePageAdmin(PageAdmin):
    inlines = [LeftColumnElementWidgetInline, RightColumnElementWidgetInline,]


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'document_listing')


class ColumnElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'content_type', 'object_id', 'site',)


class ColumnElementWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'column_element', 'page', 'max_items', 'horizontal_position', 'site')


class DocumentInline(TabularDynamicInlineAdmin):
    model = Document

    
class DocumentListingAdmin(PageAdmin):
    inlines = (DocumentInline,)


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


class SidebarBannerWidgetAdmin(admin.ModelAdmin):
    model = SidebarBannerWidget
    list_display = ('id', 'active', 'title', 'image', 'url', 'image')


class SocialMediaButtonInline(TabularDynamicInlineAdmin):
    model = SocialMediaButton
    verbose_name = "Social media buttons"
    verbose_name_plural = "Social media buttons"


class SidebarAdmin(admin.ModelAdmin):
    model = Sidebar
    inlines = (SidebarBlogCategoryWidgetInline,
               SidebarTwitterWidgetInline,
               SocialMediaButtonInline,)
    list_display = ('name', 'active', 'site')


class SidebarElementWidgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'sidebar_element', 'site')


class SocialMediaButtonGroupAdmin(admin.ModelAdmin):
    inlines = (SocialMediaButtonInline,)


admin.site.register(HomePage, HomePageAdmin)
admin.site.register(Sidebar, SidebarAdmin)
admin.site.register(SidebarBannerWidget, SidebarBannerWidgetAdmin)
admin.site.register(DocumentListing, DocumentListingAdmin)

if settings.DEBUG:
    admin.site.register(ColumnElement, ColumnElementAdmin)
    admin.site.register(ColumnElementWidget, ColumnElementWidgetAdmin)
    admin.site.register(Document, DocumentAdmin)
