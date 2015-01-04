import logging
logger = logging.getLogger(__name__)

from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from website.jdpages.models import JDPage, HomePage, ColumnElement, ColumnElementWidget, DocumentListing, Document

from website.utils.containers import HorizontalPosition


class LeftColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """"""
    model = ColumnElementWidget
    verbose_name_plural = 'Left column widgets'
    
    def queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.LEFT)


class RightColumnElementWidgetInline(TabularDynamicInlineAdmin):
    """"""
    model = ColumnElementWidget
    verbose_name_plural = 'Right column widgets'
    
    def queryset(self, request):
        return ColumnElementWidget.objects.filter(horizontal_position=HorizontalPosition.RIGHT)


class HomePageAdmin(PageAdmin):
    inlines = [LeftColumnElementWidgetInline, RightColumnElementWidgetInline,]


class ColumnElementAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'content_type', 'object_id', 'site', 'title',)


class DocumentInline(TabularDynamicInlineAdmin):
    model = Document

    
class DocumentListingAdmin(PageAdmin):
    inlines = (DocumentInline,)


admin.site.register(JDPage, PageAdmin)
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(ColumnElement, ColumnElementAdmin)
admin.site.register(ColumnElementWidget)
admin.site.register(DocumentListing, DocumentListingAdmin)
